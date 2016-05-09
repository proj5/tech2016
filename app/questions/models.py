from __future__ import unicode_literals

from django.db import models
from a2ausers.models import A2AUser
from topics.models import Topic
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete

from django.utils.functional import wraps

import inspect


class Question(models.Model):
    question = models.CharField(max_length=400)
    detail = models.TextField(null=True, blank=True)
    posted_by = models.ForeignKey(A2AUser, related_name="recent_questions")
    followed_by = models.ManyToManyField(
        A2AUser,
        related_name="followed_questions",
        blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    num_answers = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    topics = models.ManyToManyField(
        Topic,
        related_name="questions",
        blank=True
    )

    def __unicode__(self):
        return self.question


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == 'loaddata':
                return
        signal_handler(*args, **kwargs)
    return wrapper


@receiver(m2m_changed, sender=Question.topics.through)
@disable_for_loaddata
def add_question(sender, action, instance, reverse, **kwargs):
    if not reverse:
        if action == 'post_add':
            for topic in instance.topics.all():
                topic.num_questions += 1
                topic.save()


@receiver(pre_delete, sender=Question)
def delete_question(sender, instance, **kwargs):
    for topic in instance.topics.all():
        if topic.num_questions > 0:
            topic.num_questions -= 1
            topic.save()
