from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


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


class AuthenticationApiTest(APITestCase):
    fixtures = ['auth', 'users']

    def test_login_success(self):
        url = '/api/v1/auth/login/'
        # Success login
        data = {'username': 'user', 'password': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        url = '/api/v1/auth/login/'
        # Wrong password
        data = {'username': 'user', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_no_account(self):
        url = '/api/v1/auth/login/'
        # No account
        data = {'username': 'abc', 'password': 'abc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register(self):
        register_url = '/api/v1/accounts/'
        login_url = '/api/v1/auth/login/'

        # Create user and then login
        data = {
            'user': {
                'username': 'abc',
                'password': 'abc',
                'email': 'abc@example.com'
            }
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'username': 'abc', 'password': 'abc'}
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
