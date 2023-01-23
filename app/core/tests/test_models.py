"""Tests for models"""

from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self) -> None:
        """Test a successful user creation flow"""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email, password)  # type: ignore
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self) -> None:
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

    def test_new_user_without_email_error(self) -> None:
        """Test if creating user without email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")  # type: ignore

    def test_create_superuser(self) -> None:
        user = get_user_model().objects.create_superuser("test@example.com", "testpass123")  # type: ignore # noqa

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self) -> None:
        """Test creating a recipe is successful"""

        user = get_user_model().objects.create_user("test@example.com", "testpass123")  # type: ignore
        recipe = models.Recipe.objects.create(
            user=user,
            title="Simple recipe name",
            time_minutes=5,
            price=Decimal(5.50),
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)
