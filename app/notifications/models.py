from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from a2ausers.models import A2AUser
from answers.models import Answer
from questions.models import Question


class Notification(models.Model):
    NOTI_TYPES = (
        ('01', 'USER comments on followed ANSWER'),
        ('02', 'USER answers followed QUESTION'),
        ('03', 'USER upvotes/downvotes ANSWER')
    )
    type = models.CharField(max_length=200, choices=NOTI_TYPES)
    parent_id = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(A2AUser, related_name="notifications")
    created_by = models.ForeignKey(
        A2AUser,
        related_name="notification_created"
    )


@receiver(post_save, sender=Notification)
def add_noti(sender, instance, created, raw, **kwargs):
    if created and not raw:
        obj = None
        try:
            if instance.type == '01':
                obj = Answer.objects.get(pk=instance.parent_id)
            elif instance.type == '02':
                obj = Question.objects.get(pk=instance.parent_id)
            else:
                obj = Answer.objects.get(pk=instance.parent_id)
        except:
            raise Exception('Parent id does not exist')
        print obj
        if instance.user.id == instance.created_by.id:
            raise Exception('user and created_by must be different')
