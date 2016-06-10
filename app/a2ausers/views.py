import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash

from rest_framework import permissions, status, views
from rest_framework.response import Response

from a2ausers.models import A2AUser, User
from a2ausers.permissions import IsAccountOwner
from a2ausers.serializers import A2AUserSerializer, UserSerializer
from a2ausers.serializers import AvatarSerializer


class UserListView(views.APIView):

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    # Handle GET request to get list of all users
    def get(self, request, format=None):
        users = A2AUser.objects.all()
        serializer = A2AUserSerializer(users, many=True)
        return Response(serializer.data)

    # Handle POST request to create new users
    def post(self, request, format=None):
        serializer = A2AUserSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data['user']

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            # client should post facebook_id to enable this
            # facebook_id = data.get('facebook_id')
            if password != confirm_password:
                return Response({
                    'message': 'Password and confirm password don\'t match'
                }, status=status.HTTP_400_BAD_REQUEST)

            A2AUser.objects.create_user(
                username, first_name, last_name, email, password,
                **serializer.validated_data
            )

            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(views.APIView):

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def get_object(self, username):
        return A2AUser.objects.get(user__username=username)

    # Handle GET request to get a specific user
    def get(self, request, username, format=None):
        try:
            user = self.get_object(username)
            serializer = A2AUserSerializer(user)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Handle PUT request to update user profile
    def put(self, request, username, format=None):
        serializer = A2AUserSerializer(data=request.data)
        user = User.objects.get(username=username)
        self.check_object_permissions(request, user)

        if serializer.is_valid() is False:
            return Response({
                'message': 'Cannnot update profile with provided information'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        password = data['user'].get('password')
        confirm_password = data['user'].get('confirm_password')

        if password != confirm_password:
            return Response({
                'message': 'Password and confirm password don\'t match'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user,
                                         data=data['user'])

        if user_serializer.is_valid():
            user_serializer.save()

            account = self.get_object(username)
            # client should put facebook_id to enable this
            # account.facebook_id = data.get('facebook_id')
            account.save()

            update_session_auth_hash(request, user)

            return Response(A2AUserSerializer(account).data)

        return Response(user_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE request
    def delete(self, request, username, format=None):
        user_account = self.get_object(username)
        user = User.objects.get(username=username)

        self.check_object_permissions(request, user)

        user_account.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(views.APIView):

    # Handle POST request to login a user
    def post(self, request, format=None):
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = UserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Handle POST request to logout a user
    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AvatarView(views.APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    def get(self, request, username, format=None):
        # Get user's avatar
        user = A2AUser.objects.get(user__username=username)
        serializer = AvatarSerializer(user)
        return Response(serializer.data)

    def post(self, request, username):
        # Upload new avatar
        user = A2AUser.objects.get(user__username=username)
        serializer = AvatarSerializer(user, data=request.data)
        if serializer.is_valid():
            avatar = serializer.validated_data['avatar']
            user.avatar = avatar
            user.save()
            return Response(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
