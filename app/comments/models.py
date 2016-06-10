from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from a2ausers.models import A2AUser
from posts.models import Post


class Comment(models.Model):
    # COMMENT_TYPES = (
    #     ('QU', 'Comment on question'),
    #     ('AN', 'Comment on answer')
    # )
    # type = models.CharField(
    #     max_length=2,
    #     choices=COMMENT_TYPES,
    #     default='AN'
    # )
    parent = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        related_name="comments"
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(A2AUser, related_name="comments")

    def type(self):
        if self.parent.type == "question":
            return "question"
        else:
            return "answer"


@receiver(post_save, sender=Comment)
def add_comment(sender, instance, created, raw, **kwargs):
    if created and not raw:
        try:
            post = instance.parent
        except:
            post = None
            raise Exception('Question does not exist')
        if post is not None:
            post.num_comments += 1
            post.followed_by.add(instance.created_by)
            post.save()

        instance.created_by.num_comments += 1
        instance.created_by.save()


@receiver(pre_delete, sender=Comment)
def delete_comment(sender, instance, **kwargs):
    try:
        post = instance.parent
    except:
        post = None
    if post is not None and post.num_comments > 0:
        post.num_comments -= 1
        post.save()

    instance.created_by.num_comments -= 1
    instance.created_by.save()
