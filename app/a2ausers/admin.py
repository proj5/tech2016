from django.contrib import admin

from .models import A2AUser


class A2AUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user'
    ]

admin.site.register(A2AUser, A2AUserAdmin)
