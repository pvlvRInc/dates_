from rest_framework import serializers
from date.models import User


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User