from notifications.models import Notification, Read
from rest_framework import serializers
from posts.serializers import SimplePostSerializer
from a2ausers.serializers import A2AUserSerializer
from questions.serializers import SimpleQuestionSerializer


class NotificationSerializer(serializers.ModelSerializer):

    post = SimplePostSerializer()
    created_by = A2AUserSerializer()
    type = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()

    class Meta:

        model = Notification
        fields = ('id', 'type', 'post', 'created_by', 'question')

    def get_type(self, obj):
        return obj.get_type_display()

    def get_question(self, obj):
        if obj.post.type == 'answer':
            post = obj.post.parent
        else:
            post = obj.post
        question = post.question
        serializer = SimpleQuestionSerializer(question)
        return serializer.data


class ReadSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = Read
        fields = ('id', 'notification', 'read')
