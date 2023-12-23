from fastapi import Depends, HTTPException, status, APIRouter
import psycopg2
from sqlalchemy.orm import Session

from app import schemas
from models import *
from app.database import get_db
from app.utils import get_password_hash, verify_password, send_mail, generate_otp, verify_user_otp
from app import oauth2


router = APIRouter(
    prefix='/api/v1',
    tags=['Authentication']
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = get_password_hash(user.password)
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except (Exception, psycopg2.IntegrityError) as error:
        # if error.pgcode == errorcodes.UNIQUE_VIOLATION:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User already exists")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # check if user exists
    db_user = db.query(User).filter(
        User.email == user.email).first()
    # if the user doesn't exist
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user found with this email")
    # check if the password matches
    is_password_correct = verify_password(user.password, db_user.password)
    # if password doesn't match, raise an error
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    # if password matches, return login successful

    access_token = oauth2.create_access_token(data={"email": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(user: schemas.UserChangePassword, db: Session = Depends(get_db)):
    print(user)
    # check if user with provided email exists
    db_user = db.query(User).filter(
        User.email == user.email).first()
    # if the user doesn't exist, raise an error
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user found with this email")
    # check if the password matches
    is_password_correct = verify_password(user.password, db_user.password)
    # if password doesn't match, raise an error
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    # if password matches, change the password
    db_user.password = get_password_hash(user.new_password)
    db.commit()
    return {"message": "Password changed successfully!"}


@router.post("/forgot-password")
def forgot_password(user: schemas.UserForgotPassword, db: Session = Depends(get_db)):
    # check if user with provided email exists
    db_user = db.query(User).filter(
        User.email == user.email).first()
    # if the user doesn't exist, raise an error
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user found with this email")
    # if user exists, send the email
    try:
        # generate otp
        otp = generate_otp()
        send_mail(to=user.email,
                  subject="BloodBond Password Reset Request",
                  body=f"""
Dear {db_user.name},

You've requested to reset your BloodBond password. Here's your one-time password:

{otp}

Use this code to reset your password within the next 10 minutes. If you didn't make this request, please ignore this message.

Stay secure,
BloodBond Team                       
                """)
        return {"message": "Email sent successfully!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(cred: schemas.UserOtpVerify, db: Session = Depends(get_db)):
    result = verify_user_otp(cred.email, cred.otp, db)
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid otp!")
    return {"status": "Success"}


@router.post('/reset-password', status_code=status.HTTP_200_OK)
def reset_password(credential: schemas.UserResetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == credential.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No user found with given email.")
    user.password = get_password_hash(credential.password)
    db.commit()
    return {"message": "Password reset successful!"}
