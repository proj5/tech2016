from questions.models import Question
from rest_framework import serializers
from posts.serializers import PostSerializer


class QuestionSerializer(serializers.ModelSerializer):

    post = PostSerializer()

    class Meta:

        model = Question
        fields = ('id', 'question', 'post')


class QuestionWithTopAnswerSerializer(serializers.ModelSerializer):

    post = PostSerializer()
    answer = serializers.SerializerMethodField('get_top_answer')

    class Meta:
        model = Question
        fields = ('id', 'question', 'post', 'answer')

    def get_top_answer(self, obj):
        post = obj.post
        answer = post.child_posts.all().order_by('-total_vote')[0]
        serializer = PostSerializer(answer)
        return serializer.data


class SimpleQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question')
