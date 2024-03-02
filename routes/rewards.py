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
    prefix="/api/v1",
    tags=["Rewards"]
)


@router.post("/rewards/", status_code=status.HTTP_201_CREATED)
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


@router.get("/rewards/", status_code=status.HTTP_200_OK, response_model=list[schemas.RewardResponse])
def get_rewards(showAll: bool = True,  db:  Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # check if user is logged in
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Unathorized! Please login first")
    try:
        if showAll:
            return db.query(models.Reward).all()
        else:  # show only those which aren't completely redeemded
            return db.query(models.Reward).filter(models.Reward.redeemed_quantity < models.Reward.total_quantity).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.post("/redeem/{id}", status_code=status.HTTP_200_OK)
def redeem(id: int,  db:  Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    if not current_user or not current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        reward = db.query(models.Reward).filter(
            models.Reward.id == id).first()
        if reward is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found")
        if reward.redeemed_quantity >= reward.total_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Reward out of stock")
        # check if donor has enough points
        if current_user.donor.points < reward.points:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient points")
        # add redeem instance in redeem table

        new_redeem = models.Redeem(
            reward_id=id, donor_id=current_user.donor_id)
        db.add(new_redeem)
        # update donor points
        current_user.donor.points -= reward.points
        # update reward redeemed quantity
        reward.redeemed_quantity += 1

        db.commit()
        return {"message": "Reward redeemed successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/redeem", status_code=status.HTTP_200_OK, response_model=list[schemas.RedeemResponse])
def get_my_redeems(db:  Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    if not current_user or not current_user.is_donor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        return db.query(models.Redeem).filter(models.Redeem.donor_id == current_user.donor_id).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")
