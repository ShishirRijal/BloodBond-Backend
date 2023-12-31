import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, status
from PIL import Image
import uuid

from fastapi.responses import FileResponse

router = APIRouter(
    tags=["Image"],
)


@router.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile):
    return await upload_image(file)


@router.get("/get-image/{image}", response_class=FileResponse)
async def get_file(image: str):
    return await get_image(image)


# Helper functions
async def upload_image(file: UploadFile):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded!")

        # Check for allowed file formats
        allowed_formats = {".jpg", ".png"}
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in allowed_formats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File format not supported! Only .jpg and .png files are allowed."
            )

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
