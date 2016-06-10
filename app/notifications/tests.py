import json
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post, Vote
from a2ausers.models import A2AUser
from comments.models import Comment
from notifications.models import Notification, Read
# Create your tests here.


class NotificationTest(TestCase):
    fixtures = [
        'auth', 'users', 'topics', 'posts',
        'questions', 'comments', 'notifications'
    ]

    def get_notifications_per_user(self):
        result = {}
        for user in A2AUser.objects.all():
            result[user] = user.notifications.count()
        return result

    def get_users_per_notification(self):
        result = {}
        for notification in Notification.objects.all():
            result[notification] = notification.users.count()
        return result

    def setUp(self):
        self.notifications_per_user = self.get_notifications_per_user()
        self.users_per_notification = self.get_users_per_notification()

        self.admin = A2AUser.objects.get(pk=1)
        self.user = A2AUser.objects.get(pk=2)

    def check_unread_notifications(self):
        for user in A2AUser.objects.all():
            self.assertEqual(
                user.num_unread_notis,
                Read.objects.filter(user=user, read=False).count()
            )

    def check_notifications_per_user(self, change_user=[], created_by=None):
        notifications = self.get_notifications_per_user()
        for user, num_noti in self.notifications_per_user.iteritems():
            change_value = 0
            if user in change_user and user != created_by:
                change_value = 1
            self.assertEqual(num_noti + change_value, notifications[user])

    def check_users_per_notification(self):
        users = self.get_users_per_notification()
        num_noti_change = 0
        for noti, num_user in self.users_per_notification.iteritems():
            if noti in users:
                self.assertEqual(num_user, users[noti])
            else:
                num_noti_change += 1

        self.assertTrue(num_noti_change <= 1)

    def check_notification(self, notification, type, content, users):
        self.assertEqual(notification.type, type)
        self.assertEqual(notification.content, content)

        users = set(users)
        users.discard(notification.created_by)
        noti_users = set(notification.users.all())
        self.assertEqual(noti_users, users)

    def test_add_notification_when_add_comment_different_user(self):
        post = Post.objects.get(pk=1)
        pre_num_read = self.user.notifications.count()
        comment = Comment(
            parent=post,
            content='Good question',
            created_by=self.admin
        )
        comment.save()

        self.assertEqual(pre_num_read + 1, self.user.notifications.count())
        self.check_unread_notifications()
        self.check_notifications_per_user(
            post.followed_by.all(),
            comment.created_by,
        )
        self.check_users_per_notification()
        self.check_notification(
            Notification.objects.latest('created_date'),
            type='01',
            content='',
            users=post.followed_by.all()
        )

    def test_add_notification_when_add_comment_same_user(self):
        post = Post.objects.get(pk=1)
        pre_num_read = self.user.notifications.count()
        comment = Comment(
            parent=post,
            content='Good question',
            created_by=self.user
        )
        comment.save()

        self.assertEqual(pre_num_read, self.user.notifications.count())
        self.check_unread_notifications()
        self.check_notifications_per_user(
            post.followed_by.all(),
            comment.created_by
        )
        self.check_users_per_notification()
        self.check_notification(
            Notification.objects.latest('created_date'),
            type='01',
            content='',
            users=post.followed_by.all()
        )

    def test_add_notification_when_add_answer(self):
        post = Post(
            type='answer',
            parent=Post.objects.get(pk=1),
            content='Ok',
            created_by=self.admin
        )
        post.save()

        self.check_unread_notifications()
        self.check_notifications_per_user(
            post.parent.followed_by.all(),
            post.created_by
        )
        self.check_users_per_notification()
        self.check_notification(
            Notification.objects.latest('created_date'),
            type='02',
            content='',
            users=post.parent.followed_by.all()
        )

    def test_add_notification_when_vote_different_user(self):
        pre_num_read = self.admin.notifications.count()
        vote = Vote(
            post=Post.objects.get(pk=2),
            user=self.user,
            score=1
        )
        vote.save()

        self.assertEqual(pre_num_read + 1, self.admin.notifications.count())
        self.check_unread_notifications()
        self.check_notifications_per_user([self.admin])
        self.check_users_per_notification()
        self.check_notification(
            Notification.objects.latest('created_date'),
            type='03',
            content='',
            users=[self.admin]
        )

    def test_add_notification_when_vote_same_user(self):
        pre_num_read = self.admin.notifications.count()
        vote = Vote(
            post=Post.objects.get(pk=2),
            user=self.admin,
            score=1
        )
        vote.save()

        self.check_unread_notifications()
        self.assertEqual(pre_num_read, self.admin.notifications.count())
        self.check_notifications_per_user()
        self.check_users_per_notification()


class NotificationApiTest(APITestCase):

    fixtures = [
        'auth',
        'users',
        'topics',
        'posts',
        'questions',
        'comments',
        'notifications']

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_get_notifications(self):
        self.login('admin', 'admin123')
        url = '/api/v1/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            min(5, Read.objects.filter(user__id=1).count())
        )

        for read in json.loads(response.content):
            id = read['id']
            self.assertEqual(Read.objects.get(pk=id).user.id, 1)

    def test_put_notification(self):
        self.login('admin', 'admin123')
        url = '/api/v1/notifications/?readID=4'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Read.objects.get(pk=4).read)

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)
