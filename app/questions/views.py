from rest_framework import permissions, status, views
from rest_framework.response import Response
from topics.models import Topic
from topics.serializers import SimpleTopicSerializer
from questions.models import Question
from questions.serializers import QuestionSerializer, SimpleQuestionSerializer
from questions.serializers import QuestionWithTopAnswerSerializer
from posts.models import Post
from posts.serializers import SimplePostSerializer, PostSerializer
import difflib


class QuestionView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get questions related to keyword provided
        if request.GET.get('keyword') is not None:
            questions = [elem.question for elem in Question.objects.all()]
            question_list = difflib.get_close_matches(
                request.GET.get('keyword'),
                questions,
                10,
                0.1
            )
            result = Question.objects.all().filter(question__in=question_list)
            serializer = SimpleQuestionSerializer(result, many=True)
            return Response(serializer.data)
        else:
            # Get 'count' newest questions from startID
            startID = int(request.GET.get('startID'))
            count = int(request.GET.get('count'))
            if startID != 0:
                questions = Question.objects.all().filter(
                    id__lt=startID
                ).order_by('-id')
            else:
                questions = Question.objects.all().order_by('-id')
            result = []
            for question in questions:
                if count <= 0:
                    break
                result.append(question)
                count -= 1
            question_serializer = QuestionWithTopAnswerSerializer(
                result,
                many=True
            )
            return Response(question_serializer.data)


class QuestionDetailView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get a specific question
        if request.GET.get('questionID') is not None:
            questionID = int(request.GET.get('questionID'))
            question = Question.objects.get(pk=questionID)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)

    def post(self, request, format=None):
        # Post new question
        post = Post.objects.create(
            type='question',
            content=request.data.get('content'),
            created_by=request.user.a2ausers
        )
        question = Question.objects.create(
            question=request.data.get('question'),
            post=post
        )
        if request.data.get("topics") == "":
            question.save()
            return Response(question.id, status=status.HTTP_200_OK)

        send_topics = [int(elem)
                       for elem in str(request.data.get('topics')).split('|')]
        topics = Topic.objects.all().filter(pk__in=send_topics)
        for topic in topics:
            question.topics.add(topic)
            topic.num_questions += 1
            topic.save()
        question.save()
        return Response(question.id, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        # Update a question
        if request.GET.get('questionID') is not None:
            id = request.GET.get('questionID')
            question = Question.objects.get(pk=id)
            question.question = request.data.get('question')
            question.post.content = request.data.get('content')
            question.save()
            return Response(status=status.HTTP_200_OK)


class QuestionTopicView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get all topics for question with id specified
        if request.GET.get('questionID') is not None:
            questionID = int(request.GET.get('questionID'))
            question = Question.objects.get(pk=questionID)
            serializer = SimpleTopicSerializer(
                question.topics.all(),
                many=True
            )
            return Response(serializer.data)

    def post(self, request, format=None):
        # Add new topic to question with id specified
        questionID = request.GET.get('questionID')
        new_topic = Topic.objects.get(pk=request.data.get('id'))
        question = Question.objects.get(pk=questionID)
        topics = [topic.id for topic in question.topics.all()]
        if new_topic.id in topics:
            return Response({
                'message': 'Topic existed in question'
            }, status=status.HTTP_400_BAD_REQUEST)
        question.topics.add(new_topic)
        question.save()
        new_topic.num_questions += 1
        new_topic.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        # Remove a topic from question with id specified
        if request.GET.get('questionID') is not None:
            questionID = request.GET.get('questionID')
            delete_topic = Topic.objects.get(pk=request.data.get('id'))
            question = Question.objects.get(pk=questionID)
            topics = [topic.id for topic in question.topics.all()]
            if delete_topic.id not in topics:
                return Response({
                    'message': 'Topic not available in question'
                }, status=status.HTTP_400_BAD_REQUEST)
            question.topics.remove(topic)
            topic.num_questions -= 1
            topic.save()
            question.save()
        return Response(status=status.HTTP_200_OK)


class TopicQuestionView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get newest questions from topic
        topicID = int(request.GET.get('topicID'))
        startID = int(request.GET.get('startID'))
        count = int(request.GET.get('count'))
        try:
            topic = Topic.objects.get(pk=topicID)
        except:
            return Response({
                'message': 'Topic with topicID not exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        questions = topic.questions.all().order_by('-id')
        result = []
        for question in questions:
            if count <= 0:
                break
            if (startID != 0 and question.id < startID) or startID == 0:
                result.append(question)
                count -= 1
        serializer = SimpleQuestionSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        if request.GET.get('startID') is None:
            # Get all answers for a question
            questionID = int(request.GET.get('questionID'))
            question = Question.objects.get(pk=questionID)
            post = question.post
            answers = PostSerializer(post.child_posts.all(), many=True)
            return Response(answers.data)
        else:
            # Get 'count' answers of question from startID
            questionID = int(request.GET.get('questionID'))
            startID = int(request.GET.get('startID'))
            count = int(request.GET.get('count'))
            try:
                question = Question.objects.get(pk=questionID)
            except:
                return Response({
                    'message': 'Question not exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            answers = question.post.child_posts.all().order_by('-id')
            result = []
            for answer in answers:
                if count <= 0:
                    break
                if (startID != 0 and answer.id < startID) or (startID == 0):
                    result.append(answer)
                    count -= 1
            serializer = PostSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerDetailView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def post(self, request, format=None):
        # Post new answer
        questionID = int(request.GET.get('questionID'))
        if request.data.get('content') is None:
            return Response({
                'message': 'Content not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.get(pk=questionID)
        post = question.post
        answer = Post.objects.create(
            type='answer',
            parent=post,
            content=request.data.get('content'),
            created_by=request.user.a2ausers
        )
        answer.save()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, format=None):
        # Update an answer
        answerID = int(request.GET.get('answerID'))
        post = Post.objects.get(pk=answerID)
        post.content = request.data.get('content')
        return Response(status=status.HTTP_200_OK)
