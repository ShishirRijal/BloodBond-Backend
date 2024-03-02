from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from app import schemas
from app.utils import send_notification

from routes import *
from routes import rewards

# try:
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully.")
# except Exception as e:
#     print(f"Error creating tables: {e}")


# Initialize FastAPI App
app = FastAPI()


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(rewards.router)
app.include_router(campaigns.router)
app.include_router(emergency_requests.router)
app.include_router(image.router)
app.include_router(auth.router)
app.include_router(donors.router)
app.include_router(hospitals.router)


@app.get("/", tags=["Home"])  # Homescreen Route
def root():
    return {"message": "Welcome to BloodBond!"}


@app.post("/send-notification", tags=["Notifications"])
async def here_send_notification(request: Request):
    data = await request.json()
    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    await send_notification(message)
    return {"status": "Notification sent successfully"}
