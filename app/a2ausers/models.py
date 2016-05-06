from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class A2AUser(models.Model):
    user = models.OneToOneField(User, related_name='a2ausers')
    facebook_id = models.CharField(max_length=200, null=True, blank=True)

    @property
    def user__username(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'A2A User'
        verbose_name_plural = 'A2A Users'
