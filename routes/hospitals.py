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
        # Adding to user table
        user = schemas.UserAdd(
            is_donor=False, **hospital.model_dump())
        add_user_to_db(db, user)
        return new_hospital
    except (Exception, psycopg2.IntegrityError) as error:
        print("register hospital error: ", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Hospital already exists")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


@router.get("/", response_model=list[schemas.HospitalResponseVague])
def get_donors(db: Session = Depends(get_db)):
    try:
        hospitals = db.query(models.Hospital).all()
        return hospitals
    except Exception as e:
        print(f"Get hospitals error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


@router.get("/{id}", response_model=schemas.HospitalResponse)
def get_hospital_detail(id: int, db: Session = Depends(get_db)):
    try:
        hospital = db.query(models.Hospital).filter(
            models.Hospital.id == id).first()
        if hospital is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Hospital doesn't exists")
        return hospital
    except SQLAlchemyError as e:
        print("get hospital error: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
