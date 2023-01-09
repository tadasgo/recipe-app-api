"""Tests for models"""

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test a successful user creation flow"""

        email = "test@example.com"
        password = "test_123"
        user = get_user_model().objects.create_user(email, password)
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
            user = get_user_model().objects.create_user(email, "test_123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_error(self):
        """Test if creating user without email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test_123")