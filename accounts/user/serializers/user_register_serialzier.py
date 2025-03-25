from rest_framework import serializers
from accounts.user.models import User
import uuid


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['uid', 'username', 'email', 'phone', 'password', 'first_name', 'last_name']
