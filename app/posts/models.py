from __future__ import unicode_literals

from django.db import models
from a2ausers.models import A2AUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Post(models.Model):
    POST_TYPES = (
        ('question', 'question'),
        ('answer', 'answer')
    )
    type = models.CharField(
        max_length=200,
        choices=POST_TYPES,
        default='question'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name="child_posts"
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(A2AUser, related_name="post_created")
    followed_by = models.ManyToManyField(
        A2AUser,
        related_name="followed_questions",
        blank=True
    )
    votes = models.ManyToManyField(A2AUser, through='Vote')
    total_vote = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + " , " + self.content


class Vote(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(A2AUser)
    score = models.IntegerField(default=0)


@receiver(post_save, sender=Post)
def add_answer(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.type == 'answer':
            instance.parent.question.num_answers += 1
            instance.parent.question.save()

            instance.created_by.num_answers += 1
            instance.created_by.save()
        instance.followed_by.add(instance.created_by)


@receiver(post_delete, sender=Post)
def delete_answer(sender, **kwargs):
    if kwargs.get('instance', True):
        if kwargs['instance'].type == 'answer':
            if kwargs['instance'].parent.question.num_answers > 0:
                kwargs['instance'].parent.question.num_answers -= 1
                kwargs['instance'].parent.question.save()

            instance = kwargs['instance']
            instance.created_by.num_answers -= 1
            instance.created_by.save()
