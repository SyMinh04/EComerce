from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from accounts.auth_user.models import AuthUser
from core.enums.user_type import UserType
from utils.uuid import generate_uuid


class User(AuthUser, DjangoCassandraModel):
    uid = columns.UUID(primary_key=True, default=generate_uuid)

    __user_type__ = UserType.USER.value
    _password = None
    __table_name__ = 'users'

    class Meta:
        abstract = False


    def __str__(self):
        return self.get_username()
