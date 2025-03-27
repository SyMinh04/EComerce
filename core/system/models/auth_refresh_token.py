import uuid

from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

from utils.uuid import generate_uuid


class AuthUserRefreshToken(DjangoCassandraModel):
    uid = columns.UUID(primary_key=True, default=generate_uuid)
    refresh_token = columns.Text(required=True)
    access_token_id = columns.UUID(required=True, index=True)
    application_id = columns.UUID(primary_key=True, required=True, partition_key=True)
    expires = columns.DateTime(required=False)
    revoked_at = columns.DateTime(required=False)
    is_revoked = columns.Boolean(default=False)
    user_id = columns.UUID(required=True, index=True)
    user_type = columns.Text(required=True)

    __table_name__ = 'auth_user_refresh_tokens'

    class Meta:
        db_table = 'auth_user_refresh_tokens'
        get_pk_field = 'uid'
