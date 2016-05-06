from django.contrib import admin

from .models import Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'question',
        'content',
        'score'
    ]

admin.site.register(Answer, AnswerAdmin)
