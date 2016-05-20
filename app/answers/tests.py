from django.test import TestCase
from rest_framework.test import APITestCase

from answers.models import Answer
from questions.models import Question
from a2ausers.models import A2AUser


class AnswerTest(TestCase):
    fixtures = ['auth', 'users', 'topics', 'questions', 'answers']

    def check_num_answers(self):
        for question in Question.objects.all():
            self.assertEqual(question.num_answers, question.answers.count())

    def test_add_answer(self):
        answer = Answer(
            question=Question.objects.get(pk=1),
            content='abc123',
            created_by=A2AUser.objects.get(pk=1),
            score=5
        )
        answer.save()
        self.check_num_answers()

    def test_delete_answer(self):
        Answer.objects.get(pk=1).delete()
        self.check_num_answers()


class AnswerApiTest(APITestCase):
    pass
