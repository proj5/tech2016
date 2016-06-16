from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from a2ausers.models import A2AUser
from posts.models import Post, Vote
from questions.models import Question


class PostTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'posts', 'questions']

    def test_add_post(self):
        post = Post(
            type='answer',
            parent=Post.objects.get(pk=1),
            content='Ok',
            created_by=A2AUser.objects.get(pk=1)
        )
        post.save()

        self.assertEqual(
            set(post.followed_by.all()),
            set([A2AUser.objects.get(pk=1)])
        )

        post = Post(
            type='question',
            content='Ok',
            created_by=A2AUser.objects.get(pk=2)
        )
        post.save()

        self.assertEqual(
            set(post.followed_by.all()),
            set([A2AUser.objects.get(pk=2)])
        )


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
        pre_upvote_num = Vote.objects.filter(
            post__pk=post_id, score=1
        ).count()
        pre_downvote_num = Vote.objects.filter(
            post__pk=post_id, score=-1
        ).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.data['total_vote'],
            pre_upvote_num - pre_downvote_num + 1
        )
        self.assertEqual(
            response.data['my_vote'],
            1
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            pre_upvote_num + 1,
            Vote.objects.filter(post__pk=post_id, score=1).count()
        )
        self.assertEqual(
            pre_downvote_num,
            Vote.objects.filter(post__pk=post_id, score=-1).count()
        )

    def undo_upvote(self, post_id):
        url = '/api/v1/vote/?postID=' + str(post_id)
        data = {
            'score': 1
        }
        pre_upvote_num = Vote.objects.filter(
            post__pk=post_id, score=1
        ).count()
        pre_downvote_num = Vote.objects.filter(
            post__pk=post_id, score=-1
        ).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['total_vote'],
            pre_upvote_num - pre_downvote_num - 1
        )
        self.assertEqual(
            response.data['my_vote'],
            0
        )
        self.assertEqual(
            pre_upvote_num - 1,
            Vote.objects.filter(post__pk=post_id, score=1).count()
        )
        self.assertEqual(
            pre_downvote_num,
            Vote.objects.filter(post__pk=post_id, score=-1).count()
        )

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
        pre_upvote_num = Vote.objects.filter(score=1).count()
        pre_downvote_num = Vote.objects.filter(score=-1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score + 1, post.total_vote)

        self.assertEqual(pre_upvote_num + 1,
                         Vote.objects.filter(score=1).count())
        self.assertEqual(pre_downvote_num,
                         Vote.objects.filter(score=-1).count())

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
        pre_upvote_num = Vote.objects.filter(score=1).count()
        pre_downvote_num = Vote.objects.filter(score=-1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score - 1, post.total_vote)

        self.assertEqual(pre_upvote_num,
                         Vote.objects.filter(score=1).count())
        self.assertEqual(pre_downvote_num + 1,
                         Vote.objects.filter(score=-1).count())

    def test_downvote_after_upvote_then_undo_success(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/vote/?postID=4'

        # Upvote
        self.upvote(4)
        self.undo_upvote(4)

        # Downvote
        data = {
            'score': -1
        }
        pre_vote_score = Post.objects.get(id=4).total_vote
        pre_upvote_num = Vote.objects.filter(score=1).count()
        pre_downvote_num = Vote.objects.filter(score=-1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score - 1, post.total_vote)

        self.assertEqual(pre_upvote_num,
                         Vote.objects.filter(score=1).count())
        self.assertEqual(pre_downvote_num + 1,
                         Vote.objects.filter(score=-1).count())

    def test_downvote_while_upvoted_fail(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/vote/?postID=4'

        # Upvote
        self.upvote(4)

        # Downvote
        data = {
            'score': -1
        }
        pre_vote_score = Post.objects.get(id=4).total_vote
        pre_upvote_num = Vote.objects.filter(score=1).count()
        pre_downvote_num = Vote.objects.filter(score=-1).count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        post = Post.objects.get(id=4)
        self.assertEqual(pre_vote_score, post.total_vote)

        self.assertEqual(pre_upvote_num,
                         Vote.objects.filter(score=1).count())
        self.assertEqual(pre_downvote_num,
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


class FollowPostApiTest(APITestCase):
    fixtures = ['auth', 'users', 'posts']

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def follow(self, post_id, sucessful):
        url = '/api/v1/follow/?postID=' + str(post_id)

        pre_followed_num = Post.objects.get(id=post_id).followed_by.count()
        response = self.client.post(url)

        if sucessful:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(pre_followed_num + 1,
                             Post.objects.get(id=post_id).followed_by.count())
        else:
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(pre_followed_num,
                             Post.objects.get(id=post_id).followed_by.count())

    def unfollow(self, post_id, sucessful):
        url = '/api/v1/follow/?postID=' + str(post_id)

        pre_followed_num = Post.objects.get(id=post_id).followed_by.count()
        response = self.client.post(url)

        if sucessful:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(pre_followed_num - 1,
                             Post.objects.get(id=post_id).followed_by.count())
        else:
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(pre_followed_num,
                             Post.objects.get(id=post_id).followed_by.count())

    def get_follow_status(self, post_id):
        url = '/api/v1/follow/?postID=' + str(post_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_follow_success(self):
        self.login('admin', 'admin123')

        self.follow(1, True)

    def test_unfollow_success(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.unfollow(4, True)

    def test_unfollow_then_unfollow_sucess(self):
        self.login('admin', 'admin123')

        self.follow(1, True)
        self.unfollow(1, True)

    def test_get_followed_status(self):
        self.login('admin', 'admin123')

        status = self.get_follow_status(4)
        self.assertEqual(status, 1)

        status = self.get_follow_status(1)
        self.assertEqual(status, 0)

        self.follow(1, True)
        status = self.get_follow_status(1)
        self.assertEqual(status, 1)
