import smtplib
from typing import Optional

from email.message import EmailMessage

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from API.auth.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from API.auth.database import User, get_user_db


def get_email_template_registration(username: str, email_address: str):
    message = EmailMessage()
    message['Subject'] = 'Welcome to our service!'
    message['From'] = SMTP_USER
    message['To'] = email_address

    message.set_content(
        '<body>' 
        f'<h1> Welcome {username}! </h1>' 
        '<p> You have successfully registered. </p>' 
        '</body>',
        subtype='html'
    )

    return message


def send_email_registration(user: User):
    email = get_email_template_registration(user.nickname, user.email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    # verification_token_secret = SECRET_VERIFICATION

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        send_email_registration()


    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
