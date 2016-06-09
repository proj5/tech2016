from posts.models import Post, Vote
from rest_framework import serializers
from a2ausers.serializers import A2AUserSerializer


class PostSerializer(serializers.ModelSerializer):
    created_by = A2AUserSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'type',
            'content',
            'created_date',
            'created_by',
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
