from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
import models

router = APIRouter(
    prefix="/api/v1/donors",
    tags=["Donors"]
)


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
