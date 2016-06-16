from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from a2ausers.models import A2AUser
from posts.models import Post, Vote
from comments.models import Comment
from a2ausers.serializers import A2AUserSerializer

from pusher import Pusher


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


# save answer
@receiver(post_save, sender=Post)
def add_answer(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.type == 'answer':
            notification = Notification(
                type='02',
                post=instance,
                created_by=instance.created_by,
                content=''
            )
            notification.save()
            for user in instance.parent.followed_by.all():
                if user != instance.created_by:
                    read = Read(
                        notification=notification,
                        user=user,
                    )
                    read.save()


@receiver(post_save, sender=Comment)
def add_comment(sender, instance, created, raw, **kwargs):
    if created and not raw:
        try:
            post = instance.parent
        except:
            post = None
            raise Exception('Post does not exist')
        if post is not None:
            notification = Notification(
                type='01',
                post=post,
                created_by=instance.created_by,
                content=''
            )
            notification.save()

            for user in instance.parent.followed_by.all():
                if user != instance.created_by:
                    read = Read(
                        notification=notification,
                        user=user,
                    )
                    read.save()


@receiver(post_save, sender=Vote)
def add_vote(sender, instance, created, raw, **kwargs):
    if created and not raw:
        try:
            post = instance.post
        except:
            post = None
            raise Exception('Post does not exist')
        if post is not None:
            notification = Notification(
                type='03',
                post=post,
                created_by=instance.user,
                content=''
            )
            notification.save()

            if instance.user != post.created_by:
                read = Read(
                    notification=notification,
                    user=post.created_by
                )
                read.save()

# calling save when not create is only when change read to true


@receiver(post_save, sender=Read)
def save_read(sender, instance, created, raw, **kwargs):
    if not raw:
        if created:
            instance.user.num_unread_notis += 1
            instance.user.save()
            user = instance.user
            channel = "notification_" + user.user.username
            pusher = Pusher("216867", "df818e2c5c3828256440",
                            "5ff000997a9df3464eb5")

            serializer = A2AUserSerializer(user)
            event_data = serializer.data
            pusher.trigger(channel, 'new_noti', event_data)
        else:
            instance.user.num_unread_notis -= 1
            instance.user.save()
