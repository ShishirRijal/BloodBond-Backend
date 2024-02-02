from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import *

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
app.include_router(campaigns.router)
app.include_router(emergency_requests.router)
app.include_router(image.router)
app.include_router(auth.router)
app.include_router(donors.router)
app.include_router(hospitals.router)


@app.get("/", tags=["Home"])  # Homescreen Route
def root():
    return {"message": "Welcome to BloodBond!"}
