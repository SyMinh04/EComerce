from core.repositories import BaseRepository
from core.system.models import AuthUserAccessToken


class AuthAccessTokenRepository(BaseRepository):
    def __init__(self):
        self.model = AuthUserAccessToken

    def find_by_token(self, token: str):
        """
        Find access token by token
        :param token:
        :return:
        """
        return self.filter(access_token=token).first()
    def find_by_uid(self, uid: str):
        """
        Find access token by uid
        :param uid:
        :return:
        """
        return self.filter(uid=uid).first()
