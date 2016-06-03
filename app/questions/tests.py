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

        self.assertEqual(
            Question.objects.count(),
            Post.objects.filter(parent__isnull=True).count()
        )

    def check_num_answers(self):
        for question in Question.objects.all():
            self.assertEqual(
                question.num_answers,
                Post.objects.filter(parent=question.post).count()
            )

    def test_create_question(self):
        post = Post(
            content='Testing',
            created_by=A2AUser.objects.get(pk=1)
        )
        post.save()

        question = Question(
            question='Test',
            post=post
        )
        question.save()

        question.topics.add(Topic.objects.get(pk=1))
        self.check_num_answers()
        self.check_num_questions()

    def test_add_answer_to_question(self):
        post = Post(
            content='Testing',
            type='answer',
            parent=Question.objects.get(pk=1).post,
            created_by=A2AUser.objects.get(pk=1)
        )
        post.save()

        self.check_num_answers()
        self.check_num_questions()

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
        pre_num_question = Question.objects.count()
        Question.objects.get(pk=1).delete()
        self.assertEqual(Question.objects.count(), pre_num_question - 1)
        self.check_num_answers()
        self.check_num_questions()


class QuestionApiTest(APITestCase):
    pass
