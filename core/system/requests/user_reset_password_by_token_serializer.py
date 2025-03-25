from rest_framework import serializers

from core.serializers.requests import BaseRequestSerializer


class UserResetPasswordByTokenSerializer(BaseRequestSerializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
