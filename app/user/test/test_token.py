from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token_obtain_pair')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TokenApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
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

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

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

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
