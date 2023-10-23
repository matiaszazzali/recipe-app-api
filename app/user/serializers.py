"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:  # specify which model we want to serialize
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # overwrite the default "create method" of the serializer
    # this new method is called only after the validation is done
    def create(self, valildated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**valildated_data)
