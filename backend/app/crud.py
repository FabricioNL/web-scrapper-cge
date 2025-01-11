from sqlalchemy.orm import Session
from sqlalchemy import func 
from datetime import datetime, timedelta
from app.models import Flood, Subprefecture, SubprefectureFloodCount

def get_floods_last_month(db: Session):
    last_month = (datetime.now() - timedelta(days=30)).date()  # Converte para "date"
    return db.query(Flood).filter(Flood.data >= last_month).count()

def get_floods_by_subprefecture(db: Session):
    result = db.query(Subprefecture.nome, func.count(Flood.id).label("count"))\
        .join(Flood, Flood.subprefeitura_id == Subprefecture.id)\
        .group_by(Subprefecture.nome)\
        .all()

    # Transformar em uma lista de dicionários
    return [SubprefectureFloodCount(subprefeitura=row[0], count=row[1]) for row in result]

def get_all_floods(db: Session):
    return db.query(Flood).all()