from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'post',
        'content',
        'list_user',
        'created_by'
    ]

    def list_user(self, obj):
        return "\n".join([user.username for user in obj.users.all()])

admin.site.register(Notification, NotificationAdmin)
