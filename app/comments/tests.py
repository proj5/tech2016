from django.test import TestCase
from rest_framework.test import APITestCase

from comments.models import Comment
from a2ausers.models import A2AUser
from questions.models import Question
from answers.models import Answer


class CommentTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'questions', 'answers', 'comments']

    def check_num_comments(self):
        for question in Question.objects.all():
            self.assertEqual(
                question.num_comments,
                Comment.objects.filter(
                    type='QU',
                    parent_id=question.pk).count())

    def test_add_comment_to_non_exist_question(self):
        try:
            comment = Comment(
                type='QU',
                parent_id=10,
                created_by=A2AUser.objects.get(pk=1)
            )
            comment.save()
        except:
            return

        self.assertFalse(True, 'Should throw exception')

    def test_add_comment_to_non_exist_answer(self):
        try:
            comment = Comment(
                type='AN',
                parent_id=10,
                created_by=A2AUser.objects.get(pk=1)
            )
            comment.save()
        except:
            return

        self.assertFalse(True, 'Should throw exception')

    def test_add_comment_to_question(self):
        comment = Comment(
            type='QU',
            parent_id=1,
            created_by=A2AUser.objects.get(pk=1)
        )
        comment.save()
        self.check_num_comments()

    def test_delete_comment_of_question(self):
        Comment.objects.get(pk=2).delete()
        self.check_num_comments()


class CommentApiTest(APITestCase):
    pass
