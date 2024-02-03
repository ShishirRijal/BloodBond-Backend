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
    prefix="/api/v1/campaigns",
    tags=["Donation Campaigns"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_emergency_request(request: schemas.CampaignCreate, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # donors cannot create emergency requests
    if not current_user or current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        id = current_user.donor_id if current_user.is_donor else current_user.hospital_id
        new_request = models.Campaign(
            **request.model_dump(), hospital_id=id)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return {"message": "Campaign created successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/", response_model=list[schemas.CampaignResponse], status_code=status.HTTP_200_OK)
def get_all_emergency_requests(db: Session = Depends(get_db)):
    try:
        return db.query(models.Campaign).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
