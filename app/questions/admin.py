from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'num_answers',
        'get_topics'
    )

    def get_topics(self, obj):
        return ",".join([topic.name for topic in obj.topics.all()])

admin.site.register(Question, QuestionAdmin)
