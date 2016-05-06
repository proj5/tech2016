from django.contrib import admin

from .models import Topic


class TopicAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = (
        'id',
        'name',
        'num_questions'
    )

admin.site.register(Topic, TopicAdmin)
