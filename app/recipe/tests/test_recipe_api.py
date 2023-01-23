"""Tests for recipe APIs"""

from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user: str, **params) -> Recipe:
    """Create and return a sample recipe"""

    defaults = {
        "title": "Sample recipe title",
        "time_minutes": 22,
        "price": Decimal("5.25"),
        "description": "Sample description",
        "link": "https://example.com/recipe.pdf",
    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITests(TestCase):
    """Test public API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        """Test auth is required to call API"""

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@example.com", "testpass123")  # type: ignore
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self) -> None:
        """Test retrieve a list of recipes"""

        create_recipe(self.user)
        create_recipe(self.user)

        # makes request to the api
        res = self.client.get(RECIPES_URL)

        # retrieve all recipes in reverse order
        recipes = Recipe.objects.all().order_by("-id")
        # pass recipes through serializer
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)  # type: ignore

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user"""

        other_user = get_user_model().objects.create_user("other@example.com", "testpass123")  # type: ignore

        create_recipe(other_user)
        create_recipe(self.user)

        # makes request to the api
        res = self.client.get(RECIPES_URL)

        # only get current user recipes
        recipes = Recipe.objects.filter(user=self.user)
        # pass recipes through serializer
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)  # type: ignore
