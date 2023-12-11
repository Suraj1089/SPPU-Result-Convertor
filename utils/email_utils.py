import random
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from db.schemas.user import UserInDB
from internal.config import settings
from utils.user import create_access_token, fade_data_in_html

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_LOGIN,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_LOGIN,
    MAIL_PORT=465,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(recipients: List[str], subject: str, html_body: str,
                     subtype: MessageType = MessageType.html):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=html_body,
        subtype=subtype
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_new_account_email(email_to: str, subject: Optional[str], html_body: Optional[str]):
    try:
        await send_email(recipients=[email_to], subject=subject, html_body=html_body)
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def send_password_reset_email(user: UserInDB) -> None:
    token = create_access_token(subject=user.email)
    try:
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html", encoding='utf-8') as f:
            html_template_str = f.read()
        data = {
            "project_name": settings.PROJECT_NAME,
            "username": user.email,
            "token": token,
            "valid_hours": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "link": f"{settings.WEBSITE_DOMAIN}/users/reset-password/{token}"
        }
        build_html_body = fade_data_in_html(html_template_str=html_template_str, data=data)
        await send_email(recipients=[user.email], subject="Reset Your Password",
                         html_body=build_html_body)
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def send_email_otp(user: UserInDB) -> None:
    try:
        await send_email(recipients=[user.email], subject=f"Otp to reset password is {user.otp}",
                         html_body="Thank You")
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_otp():
    return random.randint(1000, 9999)
