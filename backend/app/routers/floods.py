from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import get_floods_last_month, get_floods_by_subprefecture, get_all_floods
from app.database import get_db

router = APIRouter()

@router.get("/floods/last-month")
def last_month_floods(db: Session = Depends(get_db)):
    return {"total": get_floods_last_month(db)}

@router.get("/floods/by-subprefecture")
def floods_by_subprefecture(db: Session = Depends(get_db)):
    return get_floods_by_subprefecture(db)

@router.get("/floods/all")
def all_floods(db: Session = Depends(get_db)):
    return {"floods": get_all_floods(db)}