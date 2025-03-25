import unicodedata
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

from django.conf import settings
from django.contrib.auth.hashers import (make_password, is_password_usable)
from django.utils.crypto import salted_hmac


class AuthUser(DjangoCassandraModel):
    username = columns.Text(max_length=255)
    first_name = columns.Text(max_length=255)
    last_name = columns.Text(max_length=255)
    email = columns.Text(max_length=255)
    phone = columns.Text(max_length=20)
    is_active = columns.Boolean(default=False)
    verified_at = columns.Boolean(default=False)
    password = columns.Text(max_length=225)
    last_login = columns.Text(default=None)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    _password = None

    __user_type__ = None
    __enable_mfa__ = False
    __abstract__ = True

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True



    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    def get_user_type(self):
        """
        Get user type
        """
        return self.__user_type__

    def set_password(self, raw_password):
        """
        Set password for this user
        """
        self.password = make_password(raw_password)
        self._password = raw_password

    def verify_password(self, raw_password):
        """
        compare password
        :param raw_password:
        :return:
        """
        return self.password == make_password(raw_password)



    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        return self._get_session_auth_hash()

    def get_session_auth_fallback_hash(self):
        for fallback_secret in settings.SECRET_KEY_FALLBACKS:
            yield self._get_session_auth_hash(secret=fallback_secret)

    def _get_session_auth_hash(self, secret=None):
        key_salt = "django.contrib.auth.columns.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            secret=secret,
            algorithm="sha256",
        ).hexdigest()

    def has_perms(self, perms):
        return True

    def get_address_owner_type(self):
        return self.__user_type__
