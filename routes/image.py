import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from PIL import Image
from sqlalchemy.orm import Session
import uuid

import models
from app.database import get_db

router = APIRouter(
    tags=["Image"],
)


@router.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile):
    return await upload_image(file)


@router.get("/get-image/{image}", response_class=FileResponse)
async def get_file(image: str):
    return await get_image(image)


@router.put("/update-image/{email}", status_code=status.HTTP_201_CREATED)
async def update_file(email: str, image_link: str,    db: Session = Depends(get_db)):

    # Check if the user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        # check if the user is a donor or hospital
        if user.is_donor:
            donor = db.query(models.Donor).filter(
                models.Donor.email == email).first()
            donor.image = image_link
        else:
            hospital = db.query(models.Hospital).filter(
                models.Hospital.email == email).first()
            hospital.image = image_link
        db.commit()
        return {"message": "Image updated successfully"}
    except Exception as e:
        print(f"Update image error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred!")

# Helper functions


async def upload_image(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded!")

    # Check for allowed file formats
    allowed_formats = {".jpg", ".png", ".jpeg"}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File format not supported!"
        )
    try:
        # Open the image
        image = Image.open(file.file)

        # Generate a unique ID for the image name
        unique_id = uuid.uuid4()
        image_name = f"{unique_id}{file_extension}"

        # Save the image to the server
        script_path = Path(__file__).resolve()
        image_path = script_path.parent.parent.parent / "images" / image_name

        image.save(image_path)
        return image_name

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}"
        )


async def get_image(image: str):
    script_path = Path(__file__).resolve()
    image_path = script_path.parent.parent.parent / "images" / image
    # Check if the file exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path, media_type="image/jpeg")
