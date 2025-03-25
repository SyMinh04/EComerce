from rest_framework import serializers
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _

from core.serializers.requests import BaseRequestSerializer


class ChangePasswordSerializer(BaseRequestSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_new_password(self, value):
        """
        Validate new password
        @param value:
        @return:
        """
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        """
        Validate Serializer
        @param attrs:
        @return:
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': _("error_password_confirm_not_match")})
        return attrs
