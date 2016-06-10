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
from questions.views import QuestionView, QuestionDetailView
from questions.views import QuestionTopicView, TopicQuestionView
from questions.views import AnswerView, AnswerDetailView
from a2ausers.views import UserListView, LoginView, LogoutView, UserDetailView
from a2ausers.views import AvatarView
from comments.views import CommentView, CommentsForPostView
from posts.views import VoteView
from posts.views import PostDetailView, FollowPostView
from notifications.views import ReadView
from A2A.views import IndexView

urlpatterns = [
    # User views
    url(r'^api/v1/account/avatar/(?P<username>.+)/$', AvatarView.as_view()),
    url(r'^api/v1/accounts/(?P<username>.+)/$', UserDetailView.as_view(),
        name='detail'),
    url(r'^api/v1/accounts/', UserListView.as_view(), name='list'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),

    # Comment views
    url(r'^api/v1/comments/(?P<id>.+)/$', CommentsForPostView.as_view(),
        name='list_comments'),
    url(r'^api/v1/comment/(?P<id>.+)/$', CommentView.as_view(),
        name='create_edit_comment'),

    # Vote views
    url(r'^api/v1/vote/$', VoteView.as_view(), name='vote'),

    # Follow views
    url(r'^api/v1/follow/$', FollowPostView.as_view(), name='follow_post'),

    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/topic/question/$', TopicQuestionView.as_view()),
    url(r'^api/v1/topic/(?P<topic_id>.+)/$', TopicDetailView.as_view()),
    url(r'^api/v1/topics/$', TopicView.as_view()),
    url(r'^api/v1/topic/$', TopicDetailView.as_view()),
    url(r'^api/v1/question/topic/$', QuestionTopicView.as_view()),
    url(r'^api/v1/questions/newest/$', QuestionView.as_view()),
    url(r'^api/v1/questions/$', QuestionView.as_view()),
    url(r'^api/v1/question/$', QuestionDetailView.as_view()),
    url(r'^api/v1/answers/$', AnswerView.as_view()),
    url(r'^api/v1/answer/$', AnswerDetailView.as_view()),

    # Notification views
    url(r'^api/v1/notifications/$', ReadView.as_view()),

    url(r'^api/v1/post/(?P<id>.+)/$', PostDetailView.as_view()),
    url('^.*$', IndexView.as_view())
]
