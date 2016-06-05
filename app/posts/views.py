from rest_framework import permissions, views
from rest_framework.response import Response
from posts.models import Post
from posts.serializers import PostSerializer


class PostDetailView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, id, format=None):
        # Get single post
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
