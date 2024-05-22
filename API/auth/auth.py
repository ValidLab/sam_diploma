from fastapi_users.authentication import AuthenticationBackend, JWTStrategy
from fastapi_users.authentication import CookieTransport
from API.auth.config import SECRET_JWT


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_JWT, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_max_age=36000, cookie_httponly=False, cookie_secure=False)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
