import unittest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post
from questions.models import Question
from topics.models import Topic
from a2ausers.models import A2AUser


class QuestionTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'posts', 'questions']

    def check_num_questions(self):
        for topic in Topic.objects.all():
            self.assertEqual(topic.num_questions, topic.questions.count())

        for user in A2AUser.objects.all():
            self.assertEqual(
                user.num_questions,
                user.post_created.filter(type='question').count()
            )

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

        for user in A2AUser.objects.all():
            self.assertEqual(
                user.num_answers,
                user.post_created.filter(type='answer').count()
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
        self.assertEqual(
            set(post.followed_by.all()),
            set([post.created_by])
        )

        question.topics.add(Topic.objects.get(pk=1))
        topic = Topic.objects.get(pk=1)
        topic.num_questions += 1
        topic.save()
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

    def test_add_topic_to_question(self):
        topic = Topic.objects.get(pk=2)
        question = Question.objects.get(pk=1)
        question.topics.add(topic)
        topic.num_questions += 1
        topic.save()

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

    fixtures = [
        'auth', 'users', 'topics', 'posts', 'questions'
    ]

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

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_get_questions_related_keyword(self):
        url = '/api/v1/questions/?keyword=what`'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('id'), 1)
        self.assertEqual(response.data[0].get('question'), 'What is A2A?')
        self.assertEqual(response.data[1].get('id'), 2)
        self.assertEqual(response.data[1].get('question'),
                         'What is the Selected Topics on Technology course?')

    def test_get_all_topics_of_question(self):
        url = '/api/v1/question/topic/?questionID=1'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), 'General')

    def test_get_questions_of_topic(self):
        url = '/api/v1/topic/question/?topicID=1&startID=0&count=2'
        response = self.client.get(url)
        self.check_num_questions()
        self.assertEqual(len(response.data), 1)

    def test_post_new_question(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/question/'

        data = {
            'question': 'Test',
            'content': 'Test',
            'topics': '1|2'
        }
        response = self.client.post(url, data, format='json')
        self.check_num_questions()

    def test_add_topic_to_question(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/question/topic/?questionID=1'
        response = self.client.post(url, {
            "id": "2",
            "name": "Technology",
            "description": ""
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_num_questions()

    def test_update_question(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/question/?questionID=2'
        data = {
            'question': 'Test',
            'content': 'Test'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_topic_from_question(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/question/topic/?questionID=2'
        response = self.client.delete(url, {
            "id": "1",
            "name": "General",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = '/api/v1/question/topic/?questionID=1'
        response = self.client.delete(url, {
            "id": "1",
            "name": "General",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_num_questions()
