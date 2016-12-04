from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
