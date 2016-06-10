from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'parent',
        'content',
        'created_date',
        'last_updated',
        'created_by',
        'list_vote',
        'total_vote',
        'num_comments'
    )

    def list_vote(self, obj):
        return "\n".join([user.user.username for user in obj.votes.all()])

admin.site.register(Post, PostAdmin)
