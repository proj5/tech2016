from django.contrib import admin

from .models import Notification, Read


class ReadInline(admin.TabularInline):
    model = Read
    extra = 1


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'post',
        'content',
        'list_user',
        'created_by'
    ]
    inlines = (ReadInline,)

    def list_user(self, obj):
        return "\n".join([user.user.username for user in obj.users.all()])

admin.site.register(Notification, NotificationAdmin)
