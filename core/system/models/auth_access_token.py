from cassandra.cqlengine import columns
from django.utils import timezone
from django.utils.timezone import now
from django_cassandra_engine.models import DjangoCassandraModel

from core.system.enums import AuthApplicationGrantType


class AuthUserAccessToken(DjangoCassandraModel):
    user_id = columns.UUID(primary_key=True, partition_key=True, required=True)
    user_type = columns.Text(required=True)
    scopes = columns.Text(required=False)
    application_id = columns.UUID(required=True, index=True)

    access_token = columns.Text(required=False)
    grant_from = columns.Text(max_length=20, default=AuthApplicationGrantType.UNKNOWN.value, required=False)

    source_refresh_token_id = columns.UUID(required=False)
    grant_by_user_id = columns.UUID(required=False)
    geo_id = columns.UUID(required=False)

    is_revoked = columns.Boolean(default=False)
    revoked_at = columns.DateTime(required=False)
    expires = columns.DateTime(required=False)

    is_mfa_verified = columns.Boolean(default=False)
    mfa_required = columns.Boolean(default=False)

    _application = None
    _user = None

    __table_name__ = 'auth_user_access_tokens'

    class Meta:
        get_pk_field = 'uid'
        db_table = 'auth_user_access_tokens'

    def is_valid(self, scopes=None):
        """
        Checks if the access token is valid.
        @param scopes: An iterable containing the scopes to check or None
        """
        if self.is_revoked or self.revoked_at is not None:
            return False

        return not self.is_expired() and self.allow_scopes(scopes)

    def allow_scopes(self, scopes):
        """
        Check if the token allows the provided scopes

        @param scopes: An iterable containing the scopes to check
        """
        if not scopes:
            return True

        provided_scopes = set(self.scopes.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def is_expired(self):
        """
        Check token expiration with timezone awareness
        """
        if not self.expires:
            return True

        return now() >= timezone.make_aware(self.expires)
