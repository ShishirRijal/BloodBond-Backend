from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from app import schemas

from app.database import get_db
from app.utils import get_password_hash
import models
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/v1/hospitals",
    tags=["Hospitals"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.HospitalResponse)
def register_donor(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    try:
        hospital.password = get_password_hash(hospital.password)
        new_hospital = models.Hospital(**hospital.model_dump())
        db.add(new_hospital)
        db.commit()
        db.refresh(new_hospital)
        return new_hospital
    except (Exception, psycopg2.IntegrityError) as error:
        print("register hospital error: ", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Hospital already exists")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
