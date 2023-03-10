"""URL mappings for the user API"""

from django.urls import path
from user import views

app_name = "user"

# as_view() converts class based to a function view
urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
