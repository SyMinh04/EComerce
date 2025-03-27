from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from core.system.enums import AuthApplicationType, AuthApplicationGrantType
from core.system.models import AuthApplication


class Command(BaseCommand):
    help = 'To import existing oauth2 client credentials'

    def handle(self, *args, **options):
        application_name = input('Enter application name: ')
        client_id = input(f'Enter {application_name} Client ID: ')
        client_secret = input(f'Enter {application_name} Client Secret: ')

        AuthApplication.objects.create(
            application_name=f'Application-{application_name}',
            redirect_uris='',
            user=None,
            client_type=AuthApplicationType.CLIENT_CONFIDENTIAL.value,
            authorization_grant_type=AuthApplicationGrantType.PASSWORD.value,
            client_secret=make_password(client_secret),
            client_id=client_id,
        )

        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret}")
