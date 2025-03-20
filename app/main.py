from fastapi import FastAPI
from typing import *
from database import create_db_and_tables
from user.user_router import router as user_router
from restaurant.router import app as restaurant_router

app = FastAPI(title="SwiggyDemo")

app.include_router(user_router)
app.include_router(restaurant_router)

@app.on_event("startup")
def create_db():
    create_db_and_tables()


@app.get("/health_check")
def health_check():
    return {"message":"ok"}

