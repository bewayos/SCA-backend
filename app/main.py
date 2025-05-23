from fastapi import FastAPI
from app.database import engine
from app.api import cats, missions
from app import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(cats.router, prefix="/cats", tags=["Cats"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Spy Cat Agency is live"}



models.Base.metadata.create_all(bind=engine)