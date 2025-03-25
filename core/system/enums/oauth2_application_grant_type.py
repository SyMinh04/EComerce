from enum import Enum


class AuthApplicationGrantType(Enum):
    UNKNOWN = 'UNKNOWN'
    PASSWORD = 'PASSWORD'
    IMPLICIT = 'IMPLICIT'
    REFRESH = 'REFRESH_TOKEN'
