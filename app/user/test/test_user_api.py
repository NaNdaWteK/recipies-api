from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)

    def test_user_with_email_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pass_to_short_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        )

        self.assertFalse(user_exist)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        payload = {
            'email': user_data['email'],
            'password': user_data['password'],
        }
        create_user(**user_data)

        res = self.client.post(TOKEN_URL, payload)

        print(res)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        payload = {
            'email': user_data['email'],
            'password': 'badpass',
        }
        create_user(**user_data)

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        payload = {
            'email': user_data['email'],
            'password': '',
        }
        create_user(**user_data)

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
