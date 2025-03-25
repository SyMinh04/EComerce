from django.utils.translation import gettext as _
from rest_framework import status

from core.exception import APIException


class ApplicationException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, message=None, **kwargs):
        if message:
            self.default_detail = message
        super().__init__(**kwargs)
