"""Tests for user api"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status  # type: ignore
from rest_framework.test import APIClient  # type: ignore

# api url we will be testing user - app, create - endpoint
CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)  # type: ignore


user_details = {
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
        res = self.client.post(CREATE_USER_URL, user_details)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Check if user was created in the DB
        user = get_user_model().objects.get(email=user_details["email"])
        # check if passwords match
        self.assertTrue(user.check_password(user_details["password"]))
        # check if we are not returning password in response
        self.assertNotIn("password", res.data)  # type: ignore

    def test_user_with_email_exists_error(self) -> None:
        """Test if error is returned in case user with email exists"""

        create_user(**user_details)
        res = self.client.post(CREATE_USER_URL, user_details)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self) -> None:
        """Test if error is returned in case password is < 5 chars"""

        res = self.client.post(CREATE_USER_URL, {**user_details, "password": "123"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=user_details["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self) -> None:
        """Test if token is correctly generated for valid credentials"""

        create_user(**user_details)

        payload = {"email": user_details["email"], "password": user_details["password"]}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self) -> None:
        """Test if returns error in case credentials invalid"""

        create_user(**user_details)

        payload = {"email": user_details["email"], "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self) -> None:
        """Test if posting blank password returns error"""

        payload = {"email": user_details["email"], "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self) -> None:
        """Test authentication is required for the users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api request that require authentication"""

    def setUp(self) -> None:
        self.user = create_user(**user_details)
        # api testing client from framework
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self) -> None:
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})  # type: ignore

    def test_post_me_not_allowed(self) -> None:
        """Test POST is not allowed for ME endpoint"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self) -> None:
        """Updating user profile for the authenticated user"""

        payload = {"name": "New name", "password": "newpassword123"}
        res = self.client.patch(ME_URL, payload)

        # get latest user data
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
