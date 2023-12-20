import os
import smtplib
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy import Sequence
import secrets

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

# Generate 6 digit OTP


def generate_otp():
    return secrets.randbelow(10**6)
