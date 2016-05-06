from __future__ import unicode_literals

from django.db import models
from questions.models import Question
from a2ausers.models import A2AUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(A2AUser, related_name="answer_created")
    score = models.IntegerField(default=0)


@receiver(post_save, sender=Answer)
def add_answer(sender, instance, created, raw, **kwargs):
    if created and not raw:
        instance.question.num_answers += 1
        instance.question.save()


@receiver(post_delete, sender=Answer)
def delete_answer(sender, **kwargs):
    if kwargs.get('instance', True):
        if kwargs['instance'].question.num_answers > 0:
            kwargs['instance'].question.num_answers -= 1
            kwargs['instance'].question.save()
