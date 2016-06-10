from rest_framework import serializers

from a2ausers.models import A2AUser


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    lookup_field = 'username'

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        return instance


class A2AUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = A2AUser
        fields = (
            'id', 'user', 'avatar',
            'num_questions',
            'num_answers',
            'num_comments',
            'num_unread_notis',
            'num_comments',
            'num_upvotes',
            # enable this line when client update this
            # 'facebook_id', 'avatar',
        )


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = A2AUser
        fields = ('avatar',)
