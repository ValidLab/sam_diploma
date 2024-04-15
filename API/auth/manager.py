from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from API.auth.config import SECRET_VERIFICATION
from API.auth.database import User, get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    # verification_token_secret = SECRET_VERIFICATION

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # async def create(
    #     self,
    #     user_create: schemas.UC,
    #     safe: bool = False,
    #     request: Optional[Request] = None,
    # ) -> models.UP:
    #
    #     await self.validate_password(user_create.password, user_create)
    #
    #     existing_user = await self.user_db.get_by_email(user_create.email)
    #     if existing_user is not None:
    #         raise exceptions.UserAlreadyExists()
    #
    #     user_dict = (
    #         user_create.create_update_dict()
    #         if safe
    #         else user_create.create_update_dict_superuser()
    #     )
    #     password = user_dict.pop("password")
    #     user_dict["hashed_password"] = self.password_helper.hash(password)
    #
    #     created_user = await self.user_db.create(user_dict)
    #
    #     await self.on_after_register(created_user, request)
    #
    #     return created_user


    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)