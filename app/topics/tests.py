from rest_framework import status
from rest_framework.test import APITestCase


class TopicTest(APITestCase):

    fixtures = [
        'auth', 'users', 'topics', 'posts', 'questions'
    ]

    def test_get_all_topics_of_question(self):
        url = '/api/v1/topics/?questionID=1'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), 'General')


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

    def test_add_topic_to_question(self):
        url = '/api/v1/auth/login/'
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(url, data, format='json')

        url = '/api/v1/topic/?questionID=1'
        response = self.client.post(url, {
            "id": "2",
            "name": "Technology",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_topic_from_question(self):
        url = '/api/v1/auth/login/'
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(url, data, format='json')

        url = '/api/v1/topic/?questionID=2'
        response = self.client.delete(url, {
            "id": "1",
            "name": "General",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = '/api/v1/topic/?questionID=1'
        response = self.client.delete(url, {
            "id": "1",
            "name": "General",
            "description": ""
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
