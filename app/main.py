from fastapi import FastAPI, Depends, HTTPException, status
import psycopg2
from psycopg2 import errorcodes
from sqlalchemy.orm import Session

from .import models, schemas
from .database import engine, get_db
from .utils import get_password_hash

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to BloodBond!"}


@app.post("/api/v1/signup", status_code=status.HTTP_201_CREATED)
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
