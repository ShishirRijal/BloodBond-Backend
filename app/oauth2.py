from datetime import datetime, timedelta
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .database import get_db
from models import *
from app.schemas import TokenData


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + \
        timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("token: ", token)
        payload = jwt.decode(token,  os.environ.get(
            "SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(
        User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
    # is_donor = user.is_donor
    # if is_donor:
    #     return db.query(Donor).filter(Donor.email == token_data.email).first()
    # return db.query(Hospital).filter(Hospital.email == token_data.email).first()
