from __future__ import unicode_literals

from django.db import models
from a2ausers.models import A2AUser


class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    num_questions = models.IntegerField(default=0)
    followed_by = models.ManyToManyField(
        A2AUser,
        related_name="followed_topics",
        blank=True
    )

    def __unicode__(self):
        return self.name
