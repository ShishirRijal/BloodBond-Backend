from fastapi import FastAPI, Depends, HTTPException, status
import psycopg2
from psycopg2 import errorcodes
from sqlalchemy.orm import Session

from .import models, schemas
from .database import engine, get_db
from .utils import get_password_hash, verify_password
from . import oauth2


# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to BloodBond!"}


@app.post("/api/v1/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = get_password_hash(user.password)
        new_user = models.User(**user.model_dump())
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


@app.post("/api/v1/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # check if user exists
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
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
