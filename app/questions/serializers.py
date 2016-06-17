from questions.models import Question
from rest_framework import serializers
from posts.models import Post
from posts.serializers import PostSerializer
from topics.serializers import TopicSerializer
from a2ausers.serializers import A2AUserSerializer


class QuestionSerializer(serializers.ModelSerializer):

    post = PostSerializer()

    class Meta:

        model = Question
        fields = ('id', 'question', 'post')


class QuestionWithTopAnswerSerializer(serializers.ModelSerializer):

    post = PostSerializer()
    topics = TopicSerializer(many=True)
    answer = serializers.SerializerMethodField('get_top_answer')

    class Meta:
        model = Question
        fields = ('id', 'question', 'topics', 'post', 'answer')

    def get_top_answer(self, obj):
        post = obj.post
        try:
            answer = post.child_posts.all().order_by('-total_vote')[0]
        except:
            answer = None
        serializer = PostSerializer(answer)
        return serializer.data


class SimpleQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question')


class AnswerWithQuestionSerializer(serializers.ModelSerializer):

    question = serializers.SerializerMethodField('get_question_of_answer')

    created_by = A2AUserSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'question',
            'type',
            'content',
            'created_date',
            'created_by',
            'total_vote'
        )

    def get_question_of_answer(self, obj):
        question = obj.parent.question
        serializer = QuestionSerializer(question)
        return serializer.data
