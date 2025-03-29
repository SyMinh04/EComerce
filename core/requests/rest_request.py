from rest_framework.request import Request


class ApplicationRequest(Request):
    auth_application = None
    tenant = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_auth_application(self, auth_application):
        self.auth_application = auth_application
