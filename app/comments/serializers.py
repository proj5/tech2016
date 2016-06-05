from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_date', 'created_by')
        read_only_fields = ('created_date', 'created_by')
