from rest_framework import serializers

from comments.models import Comment

from a2ausers.serializers import A2AUserSerializer


class ExtraCommentSerializer(serializers.ModelSerializer):

    created_by = A2AUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_date', 'created_by')
        read_only_fields = ('created_date', 'created_by')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_date', 'created_by')
        read_only_fields = ('created_date', 'created_by')
