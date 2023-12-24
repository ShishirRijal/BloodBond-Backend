from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from app import schemas

from app.database import get_db
from app.utils import add_user_to_db, get_password_hash
import models
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/v1/donors",
    tags=["Donors"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.DonorResponse)
def register_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    try:
        donor.password = get_password_hash(donor.password)
        new_donor = models.Donor(**donor.model_dump())
        db.add(new_donor)
        db.commit()
        db.refresh(new_donor)
        # Adding to user table
        user = schemas.UserAdd(
            is_donor=True, **donor.model_dump())
        add_user_to_db(db, user)
        return new_donor
    except psycopg2.IntegrityError as error:
        print("register donor error: ", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User already exists")
    except Exception as e:
        print(f"register donor error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


@router.get("/", response_model=list[schemas.DonorResponseVague])
def get_donors(db: Session = Depends(get_db)):
    try:
        donors = db.query(models.Donor).all()
        return donors
    except Exception as e:
        print(f"Get donors error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


@router.get("/{id}", response_model=schemas.DonorResponse)
def get_donor_detail(id: int, db: Session = Depends(get_db)):
    try:
        donor = db.query(models.Donor).filter(models.Donor.id == id).first()
        if donor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists")
        return donor
    except SQLAlchemyError as e:
        print("get user error: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
