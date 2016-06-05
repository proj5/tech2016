from posts.models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'type',
            'content',
            'created_date',
            'total_vote'
        )


class SimplePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'type',
            'content'
        )
