from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://192.168.56.1:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=['*'],
    allow_credentials=True
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
