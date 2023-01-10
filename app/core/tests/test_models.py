"""Tests for models"""

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test a successful user creation flow"""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email, password)  # type: ignore
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email is normalized for new users"""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "testpass123")  # type: ignore # noqa
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_error(self):
        """Test if creating user without email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")  # type: ignore

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser("test@example.com", "testpass123")  # type: ignore # noqa

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
