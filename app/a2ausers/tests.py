from rest_framework.test import APITestCase
from rest_framework import status

from a2ausers.models import A2AUser
# Create your tests here.


class AuthenticationApiTest(APITestCase):
    fixtures = ['auth', 'users']

    def login(self, username, password):
        url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_login_success(self):
        response = self.login('user', 'user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        response = self.login('user', '123')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_no_account(self):
        response = self.login('123', '123')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register(self):
        pre_num_user = A2AUser.objects.count()

        register_url = '/api/v1/accounts/'

        # Create user and then login
        data = {
            'user': {
                'username': 'abc',
                'password': 'abc12345',
                'confirm_password': 'abc12345',
                'email': 'abc@example.com',
                'first_name': 'Abc',
                'last_name': 'Def'
            }
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(A2AUser.objects.count(), pre_num_user + 1)

        response = self.login('abc', 'abc12345')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAccountApiTest(APITestCase):
    fixtures = ['auth', 'users']

    def test_get_user_success(self):
        url = '/api/v1/accounts/user/'
        response = self.client.get(url)

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check user data
        user_data = response.data['user']
        self.assertEqual(user_data['username'], 'user')
        self.assertEqual(user_data['email'], 'user@email.com')
        self.assertEqual(user_data['first_name'], 'User')
        self.assertEqual(user_data['last_name'], 'Nguyen')

    def test_get_user_fail(self):
        url = '/api/v1/accounts/abc/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def login(self, username, password):
        login_url = '/api/v1/auth/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(login_url, data, format='json')
        return response

    def test_update_user_success(self):
        self.login('admin', 'admin123')
        url = '/api/v1/accounts/admin/'

        data = {
            'user': {
                'username': 'admin',
                'password': 'admin456',
                'confirm_password': 'admin456',
                'email': 'abc@example.com',
                'first_name': 'Abc',
                'last_name': 'Def'
            }
        }

        response = self.client.put(url, data, format='json')
        self.client.post('/api/v1/auth/logout/')
        response = self.login('admin', 'admin456')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = A2AUser.objects.get(pk=1)
        self.assertEqual(user.user.first_name, 'Abc')

    def test_update_user_fail(self):
        self.login('user', 'user1234')
        url = '/api/v1/accounts/admin/'

        data = {
            'user': {
                'username': 'admin',
                'password': 'admin456',
                'confirm_password': 'admin456',
                'email': 'abc@example.com',
                'first_name': 'Abc',
                'last_name': 'Def'
            }
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = A2AUser.objects.get(pk=1)
        self.assertEqual(user.user.first_name, 'Admin')

    def test_delete_user_success(self):
        pre_num_user = A2AUser.objects.count()

        self.login('user', 'user1234')
        response = self.client.delete('/api/v1/accounts/user/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(A2AUser.objects.count(), pre_num_user - 1)
        self.assertFalse(
            A2AUser.objects.filter(
                user__username='user').exists())

    def test_delete_user_fail(self):
        pre_num_user = A2AUser.objects.count()

        self.login('user', 'user1234')
        response = self.client.delete('/api/v1/accounts/admin/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(A2AUser.objects.count(), pre_num_user)
        self.assertTrue(
            A2AUser.objects.filter(
                user__username='admin').exists())


class AvatarApiTest():
    pass
