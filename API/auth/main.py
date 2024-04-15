from fastapi import FastAPI

from API.auth.auth import auth_backend
from API.auth.schemas import UserRead, UserCreate
from API.auth.router import router, fastapi_users


app = FastAPI(
    title="SAM",
    description="",
    summary="",
    version="1.0",
    root_path="/api"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(router)
