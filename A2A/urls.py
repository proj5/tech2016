"""A2A URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from topics.views import TopicView, TopicDetailView

from a2ausers.views import UserListView, LoginView, LogoutView, UserDetailView
from a2ausers.views import AvatarView

urlpatterns = [
    url(r'^api/v1/accounts/avatar/(?P<username>.+)/$', AvatarView.as_view()),
    url(r'^api/v1/accounts/(?P<username>.+)/$', UserDetailView.as_view(),
        name='detail'),
    url(r'^api/v1/accounts/', UserListView.as_view(), name='list'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),

    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/topic/(?P<topic_id>.+)/$', TopicDetailView.as_view()),
    url(r'^api/v1/topics/$', TopicView.as_view()),
    url(r'^api/v1/topic/$', TopicDetailView.as_view())
]
