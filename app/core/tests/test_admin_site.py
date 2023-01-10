"""Tests for django admin modifications"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        """Create user and client"""

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(  # type: ignore
            email="admin@example.com", password="testpass123"
        )
        # every request through client will be as this user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(  # type: ignore
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_list(self):
        """Test if users are listed on page"""

        # get url for page that shows list of users inside admin
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):

        """Test if the edit user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test if create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
