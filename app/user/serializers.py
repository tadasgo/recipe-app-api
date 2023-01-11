"""Serializers for the user api view"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


# modelSerializers auto validate and save things to selected model
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        # model the serializer is representing
        model = get_user_model()
        # fields provided in request which should be saved in the model
        # only fields which we want for user to change (is_staff ❌)
        fields = ["email", "password", "name"]
        # extra metadata to different fields
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # overrides default serializer create - normalize email, hash pass
    # gets called when validation is successful, else 400
    def create(self, validated_data):
        """Create and return user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)  # type: ignore
