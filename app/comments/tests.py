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

        for user in A2AUser.objects.all():
            self.assertEqual(
                user.num_comments,
                user.comments.all().count()
            )

    def test_add_comment_to_post(self):
        post = Post(
            type='question',
            content='Ok',
            created_by=A2AUser.objects.get(pk=1)
        )
        post.save()

        comment = Comment(
            parent=post,
            created_by=A2AUser.objects.get(pk=2)
        )
        comment.save()
        self.check_num_comments()
        self.assertEqual(
            set(post.followed_by.all()),
            set([post.created_by, comment.created_by])
        )

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

        post = Post.objects.get(id=4)
        self.assertEqual(pre_num_cmt_post + 1, post.num_comments)

    def test_post_comment_not_found(self):
        url = '/api/v1/comment/id=123654/'

        pre_num_cmt = Comment.objects.count()

        # Create comment data
        data = {
            'content': 'This is a test comment'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(pre_num_cmt, Comment.objects.count())

    def test_post_comment_unauthorized(self):
        url = '/api/v1/comment/id=123654/'

        pre_num_cmt = Comment.objects.count()

        # Create comment data
        data = {
            'content': 'This is a test comment'
        }

        # Login
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(pre_num_cmt, Comment.objects.count())

    def test_post_comment_fail(self):
        url = '/api/v1/comment/id=4/'

        pre_num_cmt = Comment.objects.count()

        # Create comment data
        data = {
            'conten': 'This is a test comment'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(pre_num_cmt, Comment.objects.count())

    def test_put_comment_success(self):
        url = '/api/v1/comment/commentID=2/'

        pre_num_cmt = Comment.objects.count()

        # Create comment data
        data = {
            'content': 'Abcd'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pre_num_cmt, Comment.objects.count())
        comment = Comment.objects.get(id=2)
        self.assertEqual(comment.content, 'Abcd')

    def test_put_comment_fail(self):
        url = '/api/v1/comment/commentID=3/'

        pre_num_cmt = Comment.objects.count()

        comment = Comment.objects.get(id=3)
        pre_content = comment.content
        # Create comment data
        data = {
            'content': 'Abcd'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(pre_num_cmt, Comment.objects.count())
        comment = Comment.objects.get(id=3)
        self.assertEqual(comment.content, pre_content)

    def test_put_comment_not_found(self):
        url = '/api/v1/comment/commentID=1234501/'

        pre_num_cmt = Comment.objects.count()

        # Create comment data
        data = {
            'content': 'Abcd'
        }

        # Login
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(pre_num_cmt, Comment.objects.count())

    def tet_get_comments_from_post(self):
        url = '/api/v1/comments/id=1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
