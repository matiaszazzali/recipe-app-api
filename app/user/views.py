"""
Views for the user API.
"""
from rest_framework import generics

from user.serializers import UserSerializer


# CreateAPIView handles a http post request for creating objects
class CreateUserView(generics.CreateAPIView):
    """Create a ne user in the system."""
    serializer_class = UserSerializer
