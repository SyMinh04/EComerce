from .clients import ClientSecretGenerator, ClientIdGenerator, BaseHashGenerator
from .reset_password_token_generator import AuthUserResetPasswordTokenGenerator
from .verify_email_token_generator import AuthUserVerifyEmailTokenGenerator


__all__ = (
    'ClientSecretGenerator',
    'ClientIdGenerator',
    'BaseHashGenerator',
    'AuthUserResetPasswordTokenGenerator',
    'AuthUserVerifyEmailTokenGenerator',
)


def generate_client_id():
    """
    Generate a suitable client ID
    """
    client_id_generator = ClientIdGenerator()
    return client_id_generator.hash()


def generate_client_secret():
    """
    Generate a suitable client secret
    """
    client_secret_generator = ClientSecretGenerator()
    return client_secret_generator.hash()
