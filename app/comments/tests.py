from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from comments.models import Comment
from a2ausers.models import A2AUser
from posts.models import Post


class CommentTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'posts', 'questions', 'comments']

    def check_num_comments(self):
        for post in Post.objects.all():
            self.assertEqual(
                post.num_comments,
                Comment.objects.filter(parent=post).count()
            )

    def test_add_comment_to_post(self):
        comment = Comment(
            parent=Post.objects.get(pk=1),
            created_by=A2AUser.objects.get(pk=1)
        )
        comment.save()
        self.check_num_comments()

    def test_delete_comment_of_post(self):
        Comment.objects.get(pk=2).delete()
        self.check_num_comments()


class CommentApiTest(APITestCase):
    fixtures = ['auth', 'users', 'topics', 'posts', 'questions', 'comments']

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_comment_success(self):
        url = '/api/v1/comment/id=4/'

        pre_num_cmt = Comment.objects.count()

        post = Post.objects.get(id=4)
        pre_num_cmt_post = post.num_comments
        # Create comment data
        data = {
            'content': 'This is a test comment'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(pre_num_cmt + 1, Comment.objects.count())
        self.assertEqual(pre_num_cmt_post + 1, post.num_comments)
