from fastapi import FastAPI

from .database import engine, Base
from routes import *

try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")


# Initialize FastAPI App
app = FastAPI()


# Routes
app.include_router(auth.router)


@app.get("/")  # Homescreen Route
def root():
    return {"message": "Welcome to BloodBond!"}
