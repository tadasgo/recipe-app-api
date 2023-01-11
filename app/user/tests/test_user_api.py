"""Tests for user api"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status  # type: ignore
from rest_framework.test import APIClient  # type: ignore

# api url we will be testing user - app, create - endpoint
CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)  # type: ignore


payload = {
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test Name",
}


class PublicUserApiTests(TestCase):
    """Test the public features of user api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self) -> None:
        """Test if creating user is successful"""

        # check response
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Check if user was created in the DB
        user = get_user_model().objects.get(email=payload["email"])
        # check if passwords match
        self.assertTrue(user.check_password(payload["password"]))
        # check if we are not returning password in response
        self.assertNotIn("password", res.data)  # type: ignore

    def test_user_with_email_exists_error(self) -> None:
        """Test if error is returned in case user with email exists"""

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self) -> None:
        """Test if error is returned in case password is < 5 chars"""

        res = self.client.post(CREATE_USER_URL, {**payload, "password": "123"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
