from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'parent_id',
        'content'
    ]

admin.site.register(Comment, CommentAdmin)
