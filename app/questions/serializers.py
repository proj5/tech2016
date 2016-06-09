from questions.models import Question
from rest_framework import serializers
from posts.serializers import PostSerializer


class QuestionSerializer(serializers.ModelSerializer):

    post = PostSerializer()

    class Meta:

        model = Question
        fields = ('id', 'question', 'post')


class SimpleQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question')
