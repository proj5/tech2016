from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from a2ausers.models import A2AUser
from questions.models import Question
from answers.models import Answer


class Comment(models.Model):
    COMMENT_TYPES = (
        ('QU', 'Comment on question'),
        ('AN', 'Comment on answer')
    )
    type = models.CharField(max_length=2, choices=COMMENT_TYPES, default='AN')
    parent_id = models.IntegerField(default=0)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(A2AUser, related_name="comments")


@receiver(post_save, sender=Comment)
def add_comment(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.type == 'QU':
            try:
                question = Question.objects.get(pk=instance.parent_id)
            except:
                question = None
                raise Exception('Question does not exist')
            if question is not None:
                question.num_comments += 1
                question.save()
        else:
            try:
                answer = Answer.objects.get(pk=instance.parent_id)
            except:
                answer = None
                raise Exception('Answer does not exist')


@receiver(post_delete, sender=Comment)
def delete_comment(sender, instance, **kwargs):
    if instance.type == 'QU':
        try:
            question = Question.objects.get(pk=instance.parent_id)
        except:
            question = None
        if question is not None and question.num_comments > 0:
            question.num_comments -= 1
            question.save()
