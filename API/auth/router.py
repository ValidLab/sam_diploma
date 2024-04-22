from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from API.auth.auth import auth_backend
from API.auth.manager import get_user_manager
from API.auth.models import User

router = APIRouter(
    prefix="/user",
    tags=["Operations with users"]
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/get_user_nickname")
def get_nickname(user: User = Depends(current_user)):
    return user.nickname


@router.get("/get_user_info")
def get_info(user: User = Depends(current_user)):

    return {'id': user.id, 'email': user.email, 'nickname': user.nickname}
