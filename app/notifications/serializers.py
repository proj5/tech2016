from notifications.models import Notification, Read
from rest_framework import serializers
from posts.serializers import SimplePostSerializer
from a2ausers.serializers import A2AUserSerializer


class NotificationSerializer(serializers.ModelSerializer):

    post = SimplePostSerializer()
    created_by = A2AUserSerializer()
    type = serializers.SerializerMethodField()

    class Meta:

        model = Notification
        fields = ('id', 'type', 'post', 'created_by')

    def get_type(self, obj):
        return obj.get_type_display()


class ReadSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = Read
        fields = ('notification', 'read')
