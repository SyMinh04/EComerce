from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from core.system.enums import AuthApplicationType, AuthApplicationGrantType
from core.system.generators import generate_client_secret, generate_client_id
from core.system.models import AuthApplication


class Command(BaseCommand):
    help = 'Create Oauth Application with grant type password'

    def handle(self, *args, **options):
        application_name = input('Enter application name: ')
        random_str = get_random_string(5)
        client_secret = generate_client_secret()
        client_id = generate_client_id()
        application_name = application_name if application_name else f'Application-{random_str}'

        AuthApplication.objects.create(
            application_name=application_name,
            redirect_uris=None,
            client_type=AuthApplicationType.CLIENT_CONFIDENTIAL.value,
            authorization_grant_type=AuthApplicationGrantType.PASSWORD.value,
            client_secret=make_password(client_secret),
            client_id=client_id,
        )

        print(f"Application Name: {application_name}")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret}")
