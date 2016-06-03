from rest_framework import status
from rest_framework.test import APITestCase


class TopicDetailTest(APITestCase):

    fixtures = [
        'auth', 'users', 'topics', 'posts', 'questions'
    ]

    def test_post_new_topic(self):
        url = '/api/v1/auth/login/'
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(url, data, format='json')

        url = '/api/v1/topic/'
        response = self.client.post(url, {
            "name": "Test",
            "description": "Test"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/api/v1/topic/'
        response = self.client.post(url, {
            "name": "General",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
