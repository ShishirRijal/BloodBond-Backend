from datetime import datetime
import os
import smtplib
from fastapi import HTTPException, Request
import httpx
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy import Sequence, and_
from sqlalchemy.orm import Session
import secrets
from app import schemas

from models import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# send mail to the specified email address
def send_mail(to: str | Sequence[str], subject, body):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=os.environ.get("MY_EMAIL_ADDRESS"),
                     password=os.environ.get("EMAIL_APP_PASSWORD"))
    connection.sendmail(
        from_addr=os.environ.get("MY_EMAIL_ADDRESS"),
        to_addrs=to,
        msg=f"Subject:{subject}\n\n{body}"
    )
    connection.close()


def generate_otp():
    return secrets.randbelow(10**6)


def add_otp_to_db(db: Session, user_email, otp):
    new_otp_instance = PasswordResetToken(
        user_email=user_email, otp=otp)
    db.add(new_otp_instance)
    db.commit()
    db.refresh(new_otp_instance)


def verify_user_otp(user_email, otp, db: Session):
    db_otp = db.query(PasswordResetToken).filter(
        and_(
            PasswordResetToken.user_email == user_email,
            PasswordResetToken.otp == otp,
            PasswordResetToken.expiry_time > datetime.utcnow()
        )
    ).first()
    print(f"db_otp {db_otp}")
    if db_otp:
        return True
    else:
        return False


def add_user_to_db(db: Session, user: schemas.UserAdd):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()

# send notification


ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"
ONESIGNAL_API_KEY = os.environ.get("ONESIGNAL_API_KEY")


async def send_notification(message: str):
    onesignal_payload = {
        "app_id": "bdc6c13e-6cc3-457f-b009-e34972e9e3bf",
        "included_segments": ["Total Subscriptions"],
        "contents": {
            "en": message,
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ONESIGNAL_API_URL, json=onesignal_payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="OneSignal API request failed")

        return {"status": "Notification sent successfully"}
