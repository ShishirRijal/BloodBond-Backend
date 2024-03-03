from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import oauth2, schemas

from app.database import get_db
from app.utils import send_notification
import models
from sqlalchemy.exc import SQLAlchemyError

from models.users import User

router = APIRouter(
    prefix="/api/v1/campaigns",
    tags=["Donation Campaigns"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_campaign(request: schemas.CampaignCreate, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # donors cannot create campaigns
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
        await send_notification("There is a new donation campaign available!")
        return {"message": "Campaign created successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.get("/my-campaigns", status_code=status.HTTP_200_OK)
def get_my_campaigns(db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    try:
        print("here")
        if not current_user.is_donor:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        campaign_response = db.query(models.CampaignAttendee).filter(
            models.CampaignAttendee.donor_id == current_user.donor_id).filter(models.CampaignAttendee.donated == True).all()

        return ({"id": campaign.campaign_id, "name": campaign.campaign.title, "image": campaign.campaign.banner, "hospital_id": campaign.campaign.hospital_id,  "hospital": campaign.campaign.hospital.name} for campaign in campaign_response)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Internal Server Error: {e}")


@router.get("/", response_model=list[schemas.CampaignResponse], status_code=status.HTTP_200_OK)
def get_all_campaigns(showAll: bool = False,  db: Session = Depends(get_db)):
    try:
        if showAll:
            return db.query(models.Campaign).all()
        return db.query(models.Campaign).filter(models.Campaign.date > datetime.now()).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


@router.post("/{id}/register", status_code=status.HTTP_201_CREATED)
def register(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # if user is not a donor, they cannot register for a campaign
    if not current_user or not current_user.is_donor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")
    # check if campaign exists
    campaign = db.query(models.Campaign).where(
        models.Campaign.id == id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    try:
        attendee = models.CampaignAttendee(
            campaign_id=id, donor_id=current_user.donor_id)
        db.add(attendee)
        db.commit()
        return {"message": "Registered successfully for the campaign"}
    except SQLAlchemyError as e:
        # check if user is already registered for the campaign
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is already registered for this campaign")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Internal Server Error: {e}")


@router.put("/{campaign_id}/donate", status_code=status.HTTP_200_OK)
def donate(campaign_id: int, request: schemas.CampaignAttendeeDonate,  db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # only hospital users can mark a campaign as donated
    donor_id = request.donor_id
    if not current_user or current_user.is_donor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")
    # check if campaign exists
    campaign = db.query(models.CampaignAttendee).where(
        models.CampaignAttendee.campaign_id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    try:
        attendee = db.query(models.CampaignAttendee).where(
            models.CampaignAttendee.campaign_id == campaign_id).where(models.CampaignAttendee.donor_id == donor_id).first()
        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not registered for this campaign")
        if attendee.donated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign is already marked as donated to this user")
        attendee.donated = True
        # credit points to the donor
        donor = db.query(models.Donor).where(
            models.Donor.id == donor_id).first()
        donor.points += 100

        db.commit()
        return {"message": "Donation marked successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Internal Server Error: {e}")


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_campaign_donors(id: int, donated: bool | None = None,  db: Session = Depends(get_db)):
    try:
        donors = list[int]
        if donated is not None:
            donors = db.query(models.CampaignAttendee).where(models.CampaignAttendee.campaign_id == id).where(
                models.CampaignAttendee.donated == donated).all()
        donors = db.query(models.CampaignAttendee).where(
            models.CampaignAttendee.campaign_id == id).all()
        return {"donors": ({"id":  donor.donor.id,  "name": f"{donor.donor.first_name} { donor.donor.last_name}", "image":  donor.donor.image, "donated": donor.donated} for donor in donors),  "registered_count": len(donors), "donated_count": len([donor for donor in donors if donor.donated])}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Internal Server Error: {e}")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):

    try:
        item_query = db.query(models.Campaign).filter(models.Campaign.id == id)
        if not item_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

        # check if user is the one who created the campaign
        is_campaign_owner = db.query(models.Campaign).filter(models.Campaign.id == id).filter(
            models.Campaign.hospital_id == current_user.hospital_id).first()

        if not is_campaign_owner:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        # delete all attendees
        db.query(models.CampaignAttendee).filter(
            models.CampaignAttendee.campaign_id == id).delete()
        item_query.delete()
        db.commit()
        return {"message": "Campaign deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Internal Server Error: {e}")
