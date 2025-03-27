from datetime import timedelta

from decouple import config
AUTH_TOKEN_MAX_AGE = timedelta(days=7).total_seconds()
COOKIE_SESSION_MAX_AGE = timedelta(days=90).total_seconds()

# COOKIE settings
SESSION_COOKIE_SAMESITE = 'lax'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_LIFE_TIME = COOKIE_SESSION_MAX_AGE
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True


# JWT settings
JWT_PROVIDER = {
    'ACCESS_TOKEN_LIFETIME': AUTH_TOKEN_MAX_AGE,
    'REFRESH_TOKEN_LIFETIME': COOKIE_SESSION_MAX_AGE,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('APP_JWT_SECRET_KEY'),
    'VERIFYING_KEY': None,
}
