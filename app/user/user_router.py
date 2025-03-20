from fastapi import APIRouter,Depends
from database import get_session

router = APIRouter(prefix="/user")

@router.get("/all")
def get_all_users():
    return{"massage":"api need to be impliment"}