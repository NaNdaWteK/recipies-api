from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_obtain_pair')
ME_URL = reverse('user:me')


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

    def test_retrieve_user_with_token_is_authorized(self):
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
        auth_res = self.client.post(TOKEN_URL, payload)

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + auth_res.data['access']
        )

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    class PrivateUserApiTests(TestCase):

        def setUp(self):
            self.user = create_user(
                email='test@example.com',
                password='testpass123',
                name='Test Name',
            )

            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

        def test_retrieve_profile_success(self):
            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, {
                'name': self.user.name,
                'email': self.user.email,
            })

        def test_retrieve_profile_method_not_allowed(self):
            res = self.client.post(ME_URL)

            self.assertEqual(
                res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )

        def test_update_user_profile(self):
            payload = {'name': 'Updated name', 'password': 'newpass123'}

            res = self.client.patch(ME_URL, payload)
            self.user.refresh_from_db()

            self.assertEqual(self.user.name, payload['name'])
            self.assertTrue(self.user.check_password(payload['password']))
            self.assertEqual(res.status_code, status.HTTP_200_OK)
