from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

from core.system.enums import AuthApplicationType, AuthApplicationGrantType
from utils.uuid import generate_uuid


class AuthApplication(DjangoCassandraModel):
    uid = columns.UUID(primary_key=True, default=generate_uuid)
    application_name = columns.Text(required=False)
    client_type = columns.Text(max_length=20, default=AuthApplicationType.CLIENT_CONFIDENTIAL, required=False)
    client_id = columns.Text(required=True)
    client_secret = columns.Text(required=False)
    authorization_grant_type = columns.Text(default=AuthApplicationGrantType.PASSWORD.value, required=False)
    redirect_uris = columns.Text(required=False)
    post_logout_redirect_uris = columns.Text(required=False)
    is_active = columns.Boolean(required=False, default=True)

    __table_name__ = 'auth_applications'

    class Meta:
        get_pk_field = 'uid'
