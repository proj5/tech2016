from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'parent_id',
        'content',
        'user'
    ]

admin.site.register(Notification, NotificationAdmin)
