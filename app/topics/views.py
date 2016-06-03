from rest_framework import permissions, status, views
from rest_framework.response import Response
from topics.models import Topic
from topics.serializers import TopicSerializer
from questions.models import Question
import difflib


class TopicView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        if request.GET.get('questionID') is not None:
            questionID = request.GET.get('questionID')
            question = Question.objects.get(pk=questionID)
            serializer = TopicSerializer(question.topics.all(), many=True)
            return Response(serializer.data)
        else:
            if request.GET.get('keyword') is None:
                topics = Topic.objects.all()
                serializer = TopicSerializer(topics, many=True)
                return Response(serializer.data)
            else:
                topics = [topic.name for topic in list(Topic.objects.all())]
                related_topics = difflib.get_close_matches(
                    request.GET.get('keyword'),
                    topics,
                    10,
                    0.2
                )
                result = Topic.objects.all().filter(name__in=related_topics)
                serializer = TopicSerializer(result, many=True)
                return Response(serializer.data)


class TopicDetailView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, topic_id, format=None):
        topic = Topic.objects.get(pk=topic_id)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def exist(self, data):
        topic_names = [topic.name for topic in Topic.objects.all()]
        if data.get('name') in topic_names:
            return True
        return False

    def post(self, request, format=None):
        if request.GET.get('questionID') is None:
            if self.exist(request.data):
                return Response({
                    'message': 'Topic name exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            topic = Topic.objects.create(
                name=request.data.get('name'),
                description=request.data.get('description')
            )
            topic.save()
        else:
            new_topic = Topic.objects.get(pk=request.data.get('id'))
            question = Question.objects.get(pk=request.GET.get('questionID'))
            topics = [topic.id for topic in question.topics.all()]
            if new_topic.id in topics:
                return Response({
                    'message': 'Topic existed in question'
                }, status=status.HTTP_400_BAD_REQUEST)
            question.topics.add(topic)
            question.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        if request.GET.get('questionID') is not None:
            delete_topic = Topic.objects.get(pk=request.data.get('id'))
            question = Question.objects.get(
                pk=request.GET.get('questionID')
            )
            topics = [topic.id for topic in question.topics.all()]
            if delete_topic.id not in topics:
                return Response({
                    'message': 'Topic not available in question'
                }, status=status.HTTP_400_BAD_REQUEST)
            question.topics.remove(topic)
            question.save()
        return Response(status=status.HTTP_200_OK)
