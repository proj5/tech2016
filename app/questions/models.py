from __future__ import unicode_literals

from django.db import models
from topics.models import Topic
from posts.models import Post
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_delete

from django.utils.functional import wraps

import inspect


class Question(models.Model):
    question = models.CharField(max_length=400)
    post = models.OneToOneField(
        Post,
        null=True,
        blank=True,
        related_name="question"
    )
    num_answers = models.IntegerField(default=0)
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


@receiver(post_delete, sender=Question)
def delete_posts_in_question(sender, instance, **kwargs):
    # delete all posts, all comments belongs to the question
    post = instance.post
    for child_post in post.child_posts.all():
        for comment in child_post.comments.all():
            comment.delete()
        if child_post.type == "answer":
            child_post.delete()
    post.delete()


@receiver(pre_delete, sender=Question)
def decrease_num_questions_in_topic(sender, instance, **kwargs):
    for topic in instance.topics.all():
        if topic.num_questions > 0:
            topic.num_questions -= 1
            topic.save()
