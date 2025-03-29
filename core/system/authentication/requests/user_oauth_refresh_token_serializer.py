from django.utils.translation import gettext as _
from rest_framework import serializers

from core.system.repositories import AuthRefreshTokenRepository, AuthAccessTokenRepository


class UserRefreshTokenSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True, max_length=255)
    refresh_token = serializers.CharField(required=True)
    scope = serializers.CharField(required=True, max_length=255)

    def validate_grant_type(self, value):
        """
        Custom validation method to check if the email is unique.
        """
        if value != 'refresh_token':
            raise serializers.ValidationError(_('error_grant_type_refresh_token'))

        return value

    def validate_refresh_token(self, value):
        """
        Validate refresh_token
        """

        refresh_token = AuthRefreshTokenRepository().find_by_token(value)
        if refresh_token is None or refresh_token.is_revoked:
            raise serializers.ValidationError(_('error_refresh_token_expired_or_revoke'))

        access_token = AuthAccessTokenRepository().find_by_uid(refresh_token.access_token_id)

        if access_token is None:
            raise serializers.ValidationError(_('error_token_expired_or_revoke'))

        if access_token.mfa_required and not access_token.is_mfa_verified:
            raise serializers.ValidationError(_('error_refresh_token_unconfirm_mfa'))

        return value

    class Meta:
        fields = ['grant_type', 'scope', 'refresh_token']
