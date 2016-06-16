from rest_framework import permissions, status, views
from rest_framework.response import Response

from comments.models import Comment
from comments.permissions import IsCommentOwner
from comments.serializers import CommentSerializer, ExtraCommentSerializer

from posts.models import Post

from a2ausers.models import A2AUser


class CommentsForPostView(views.APIView):

    # Get all comments for a post (question or answer) with id specified
    def get(self, request, id, format=None):
        if id.startswith('id='):
            id = id[3:]
        else:
            return Response(
                {'Invalid id of post.'},
                status=status.HTTP_404_NOT_FOUND)

        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(
                {'No post with that id exists.'},
                status=status.HTTP_404_NOT_FOUND)
        comments = post.comments.all()
        serializer = ExtraCommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentView(views.APIView):

    def get_permissions(self):
        return (permissions.IsAuthenticated(), IsCommentOwner())

    # Post new comment for a post (question or answer) with id specified
    def post(self, request, id, format=None):
        if id.startswith('id='):
            id = id[3:]
        else:
            return Response(
                {'Invalid id of post.'},
                status=status.HTTP_404_NOT_FOUND)

        post = Post.objects.filter(id=id).first()
        # post = Post.objects.get(id=id)

        if post is None:
            return Response(
                {'No post with that id exists.'},
                status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            author = A2AUser.objects.get(user__username=request.user.username)

            comment = Comment(parent=post, content=data.get('content'),
                              created_by=author)
            comment.save()

            # post.num_comments += 1
            # post.save()

            return Response(ExtraCommentSerializer(comment).data,
                            status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Comment could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update a comment with id specified
    def put(self, request, id, format=None):
        if id.startswith('commentID='):
            id = id[10:]
        else:
            return Response(
                {'Invalid id of comment.'},
                status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response({
                'message': 'Cannnot update comment with provided information.'
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.filter(id=id).first()
        if comment is None:
            return Response(
                {'No comment has that id.'},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)

        data = serializer.validated_data
        comment.content = data.get('content')
        comment.save()

        return Response(data, status=status.HTTP_200_OK)
