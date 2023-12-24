from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from app import schemas

from app.database import get_db
from app.utils import get_password_hash
import models

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
        return new_donor
    except (Exception, psycopg2.IntegrityError) as error:
        print("register donor error: ", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User already exists")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


@router.get("/")
def get_donors(db: Session = Depends(get_db)):
    try:
        donors = db.query(models.User).filter(
            models.User.is_donor == True).all()
        return donors
    except Exception as e:
        print(f"Get donors error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
