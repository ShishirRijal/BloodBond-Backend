from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from app import oauth2, schemas

from app.database import get_db
from app.utils import add_user_to_db, get_password_hash
import models
from sqlalchemy.exc import SQLAlchemyError

from models.users import User

router = APIRouter(
    prefix="/api/v1/emergency-requests",
    tags=["Emergency Requests"]
)


@router.post("/", response_model=schemas.EmergencyRequestResponse, status_code=status.HTTP_201_CREATED)
def create_emergency_request(request: schemas.EmergencyRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # donors cannot create emergency requests
    if not current_user or current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        new_request = models.EmergencyRequest(
            **request.model_dump(), hospital_id=current_user.id)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/", response_model=list[schemas.EmergencyRequestResponse], status_code=status.HTTP_200_OK)
def get_all_emergency_requests(db: Session = Depends(get_db)):
    try:
        return db.query(models.EmergencyRequest).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.put("/{id}", status_code=status.HTTP_200_OK)
def accept_request(id: int,  db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    if not current_user or not current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        request = db.query(models.EmergencyRequest).filter(
            models.EmergencyRequest.id == id).first()
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request.accepted or request.donated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Request already accepted")
        request.accepted = True
        request.donor_id = current_user.id
        db.commit()
        return {"message": "Request accepted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
