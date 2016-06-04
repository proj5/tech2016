from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post
from questions.models import Question


class PostTest(TestCase):
    pass


class PostApiTest(APITestCase):

    fixtures = [
        'auth', 'users', 'topics', 'posts', 'questions'
    ]

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def check_num_answers(self):
        for question in Question.objects.all():
            self.assertEqual(
                question.num_answers,
                Post.objects.filter(parent=question.post).count()
            )

    def test_get_answers(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/answers/?questionID=1'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.check_num_answers()

        url = '/api/v1/answers/?questionID=2&startID=1&count=2'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

    def test_post_answer(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/answer/?questionID=1'
        data = {
            'content': 'Test'
        }
        response = self.client.post(url, data)
        self.check_num_answers()
