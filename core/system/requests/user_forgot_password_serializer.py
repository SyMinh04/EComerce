from rest_framework import serializers

from core.serializers.requests import BaseRequestSerializer


class UserForgotPasswordSerializer(BaseRequestSerializer):
    email = serializers.EmailField(required=True)
