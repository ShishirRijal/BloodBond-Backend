from datetime import datetime
import os
import smtplib
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy import Sequence, and_
from sqlalchemy.orm import Session
import secrets

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
    connection.login(user=os.getenv("MY_EMAIL_ADDRESS"),
                     password=os.getenv("EMAIL_APP_PASSWORD"))
    connection.sendmail(
        from_addr=os.getenv("MY_EMAIL_ADDRESS"),
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
