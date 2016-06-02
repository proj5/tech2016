from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from a2ausers.models import A2AUser
from posts.models import Post


class Notification(models.Model):
    NOTI_TYPES = (
        ('01', 'USER comments on your QUESTION/ANSWER'),
        ('02', 'USER answers followed QUESTION'),
        ('03', 'USER upvotes/downvotes ANSWER')
    )
    type = models.CharField(max_length=200, choices=NOTI_TYPES)
    post = models.ForeignKey(Post, null=True, related_name="noti_list")
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    users = models.ManyToManyField(
        A2AUser,
        through='Read',
        related_name="notifications"
    )
    created_by = models.ForeignKey(
        A2AUser,
        related_name="notification_created"
    )


class Read(models.Model):
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(A2AUser)
    read = models.BooleanField(default=False)


@receiver(post_save, sender=Notification)
def add_noti(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.user.id == instance.created_by.id:
            raise Exception('user and created_by must be different')
