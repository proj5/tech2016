from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post, Vote
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


class VoteApiTest(APITestCase):

    fixtures = ['auth', 'users', 'posts']

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def upvote(self, post_id):
        url = '/api/v1/vote/?postID=' + str(post_id)
        data = {
            'score': 1
        }
        pre_vote_num = Vote.objects.filter(score=1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(pre_vote_num + 1, Vote.objects.count())

    def undo_upvote(self, post_id):
        url = '/api/v1/vote/?postID=' + str(post_id)
        data = {
            'score': 1
        }
        pre_vote_num = Vote.objects.filter(score=1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pre_vote_num - 1, Vote.objects.count())

    def get_vote_status(self, post_id):
        url = '/api/v1/vote/?postID=' + str(post_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_upvote_success(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/vote/?postID=4'
        data = {
            'score': 1
        }
        pre_vote_score = Post.objects.get(id=4).total_vote
        pre_vote_num = Vote.objects.filter(score=1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score + 1, post.total_vote)

        self.assertEqual(pre_vote_num + 1,
                         Vote.objects.filter(score=1).count())

    def test_downvote_success(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/vote/?postID=4'

        # Upvote
        # self.upvote(4)
        # self.undo_upvote(4)

        # Downvote
        data = {
            'score': -1
        }
        pre_vote_score = Post.objects.get(id=4).total_vote
        pre_vote_num = Vote.objects.filter(score=-1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score - 1, post.total_vote)

        self.assertEqual(pre_vote_num + 1,
                         Vote.objects.filter(score=-1).count())

    def test_get_upvote_status_success(self):
        self.login('user', 'user1234')
        self.upvote(4)
        status = self.get_vote_status(4)
        self.assertEqual(status, 1)

    def test_get_none_status_sucess(self):
        self.login('user', 'user1234')
        status = self.get_vote_status(3)
        self.assertEqual(status, 0)
