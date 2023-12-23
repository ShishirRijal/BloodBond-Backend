from sqlalchemy import TIMESTAMP, Column, Integer, String, text

from app.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, nullable=False)
    user_email = Column(String, nullable=False, index=True)
    otp = Column(String, nullable=False, unique=True, index=True)
    # expiry time = 5 minutes
    expiry_time = Column(TIMESTAMP(timezone=True), nullable=False,
                         server_default=text('NOW() + INTERVAL \'5 minutes\''))
