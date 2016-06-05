from posts.models import Post, Vote
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


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'score')
