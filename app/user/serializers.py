"""Serializers for the user api view"""

from typing import Dict

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers  # type: ignore


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
    def create(self, validated_data: Dict):
        """Create and return user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)  # type: ignore

    # override default update method
    # validated data will be our email, password, name
    def update(self, instance, validated_data: Dict):
        """Update and return uses"""
        # remove password it will not be required
        password = validated_data.pop("password", None)
        # use existing update method
        user = super().update(instance, validated_data)

        # update password if user wants to
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    # validate method is called by the view
    def validate(self, attrs: Dict) -> Dict:
        """Validate and authenticate user"""

        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=email, password=password)

        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
