from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testingpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized_successful(self):
        sample_emails = [
            ["test1@EXample.com", "test1@example.com"],
            ["Test2@EXample.com", "Test2@example.com"],
            ["TEST3@example.COM", "TEST3@example.com"],
        ]
        password = "testingpass123"

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, password)

            self.assertEqual(user.email, expected)