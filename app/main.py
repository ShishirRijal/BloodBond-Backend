from fastapi import FastAPI

from .import models
from .database import engine
import routes


# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routes.auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to BloodBond!"}
