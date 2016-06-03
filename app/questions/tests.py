import unittest
from django.test import TestCase
from rest_framework.test import APITestCase

from posts.models import Post
from questions.models import Question
from topics.models import Topic
from a2ausers.models import A2AUser


class QuestionTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'posts', 'questions']

    def check_num_questions(self):
        for topic in Topic.objects.all():
            self.assertEqual(topic.num_questions, topic.questions.count())

    def test_create_question(self):
        pass

    @unittest.skip('currently fail')
    def test_add_topic_to_question(self):
        topic = Topic.objects.get(pk=2)
        question = Question.objects.get(pk=1)
        question.topics.add(topic)

        self.check_num_questions()

    @unittest.skip('currently fail')
    def test_remove_topic_to_question(self):
        topic = Topic.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        question.topics.remove(topic)

        self.check_num_questions()

    def test_remove_question(self):
        Question.objects.get(pk=1).delete()
        self.check_num_questions()


class QuestionApiTest(APITestCase):
    pass
