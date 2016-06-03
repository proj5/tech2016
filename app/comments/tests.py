from django.test import TestCase
from rest_framework.test import APITestCase

from comments.models import Comment
from a2ausers.models import A2AUser
from questions.models import Question
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
    pass
