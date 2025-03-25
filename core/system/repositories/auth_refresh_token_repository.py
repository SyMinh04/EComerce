from core.repositories import BaseRepository
from core.system.models import AuthUserRefreshToken


class AuthRefreshTokenRepository(BaseRepository):
    def __init__(self):
        self.model = AuthUserRefreshToken

    def find_by_token(self, token: str):
        return self.filter(refresh_token=token).first()

    def find_by_access_token_id(self, token_id: str):
        """
        Find refresh token by access_token
        """
        return self.filter(access_token_id=token_id).first()
