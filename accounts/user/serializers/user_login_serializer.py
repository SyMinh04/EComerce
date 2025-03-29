from rest_framework import serializers
from django.utils.translation import gettext as _

from core.enums.user_type import UserType
from core.system.requests import UserLoginRequestSerializer


class UserLoginSerializer(UserLoginRequestSerializer):
    def validate_scope(self, value):
        """
        Validate scope for consumer
        """
        if value != UserType.USER.value:
            raise serializers.ValidationError(_('invalid_scope'))

        return value

