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
    prefix="/api/v1/rewards",
    tags=["Rewards"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.RewardCreate, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # donors cannot create rewards
    if not current_user or current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        new_request = models.Reward(
            **request.model_dump(), owner_id=current_user.hospital_id)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return {"message": "Reward created successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.RewardResponse])
def get_rewards(showAll: bool = True,  db:  Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # check if user is logged in
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Unathorized! Please login first")
    try:
        if showAll:
            return db.query(models.Reward).all()
        else:  # show only those which aren't completely redeemded
            return db.query(models.Reward).filter(models.Reward.remaining_quantity > 0)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
