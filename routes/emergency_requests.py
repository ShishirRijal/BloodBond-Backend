from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from app import oauth2, schemas

from app.database import get_db
from app.utils import add_user_to_db, get_password_hash, send_notification
import models
from sqlalchemy.exc import SQLAlchemyError

from models.users import User

router = APIRouter(
    prefix="/api/v1/emergency-requests",
    tags=["Emergency Requests"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_emergency_request(request: schemas.EmergencyRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # donors cannot create emergency requests
    if not current_user or current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        id = current_user.donor_id if current_user.is_donor else current_user.hospital_id
        new_request = models.EmergencyRequest(
            **request.model_dump(), hospital_id=id)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        await send_notification("Emergency blood needed!")
        return {"message": "Request created successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/", response_model=list[schemas.EmergencyRequestResponse], status_code=status.HTTP_200_OK)
def get_all_emergency_requests(showAll: bool = False, db: Session = Depends(get_db)):
    try:
        if showAll:
            return db.query(models.EmergencyRequest).all()
        return db.query(models.EmergencyRequest).filter(models.EmergencyRequest.donated == False).filter(models.EmergencyRequest.expiry_time > datetime.now()).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.put("/{id}/accept", status_code=status.HTTP_200_OK)
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
        # check if the blood group matches
        if request.blood_group != current_user.donor.blood_group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Blood group does not match")

        if request.accepted or request.donated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Request already accepted")

        request.accepted = True
        request.donor_id = current_user.donor_id
        db.commit()
        return {"message": "Request accepted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.put("/{id}/donate", status_code=status.HTTP_200_OK)
def confirm_donate(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    if not current_user or current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        request = db.query(models.EmergencyRequest).filter(
            models.EmergencyRequest.id == id).first()
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request.donated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Request already donated")
        request.donated = True
        # credit points to user
        donor = db.query(models.EmergencyRequest).filter(
            models.EmergencyRequest.id == id).first().donor
        donor.points += 100
        db.commit()
        return {"message": "Donation confirmed successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        request = db.query(models.EmergencyRequest).filter(
            models.EmergencyRequest.id == id).first()
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

        # check if user is one who created the request
        is_owner = db.query(models.EmergencyRequest).filter(
            models.EmergencyRequest.id == id).first().hospital_id == current_user.hospital_id
        print("is_owner", is_owner)
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        db.delete(request)
        db.commit()
        return {"message": "Request deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
