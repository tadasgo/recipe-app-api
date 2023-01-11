"""Views for the user api"""

from rest_framework import generics
from user.serializers import UserSerializer


# CreateAPIView handles HTTP post used for creation
# Request -> URL -> View -> Serializer -> Create -> Response
class CreateUserView(generics.CreateAPIView):
    """Create new user in the system"""

    serializer_class = UserSerializer
