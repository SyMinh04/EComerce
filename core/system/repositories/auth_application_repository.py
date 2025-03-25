from core.repositories import BaseRepository
from core.system.models import AuthApplication


class AuthApplicationRepository(BaseRepository):
    def __init__(self):
        self.model = AuthApplication
