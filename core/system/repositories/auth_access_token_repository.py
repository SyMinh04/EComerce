from core.repositories import BaseRepository
from core.system.models import AuthUserAccessToken


class AuthAccessTokenRepository(BaseRepository):
    def __init__(self):
        self.model = AuthUserAccessToken

    def find_by_token(self, token: str):
        return self.filter(access_token=token).first()
