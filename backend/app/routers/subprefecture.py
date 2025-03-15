from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import get_all_subprefectures
from app.database import get_db
router = APIRouter()

"""
_summary_
cria uma rota para retornar os ids e nomes das subprefeituras

_parameters_
db: Session = Depends(get_db) -> sessão do banco de dados

_returns_
subprefeituras: lista de dicionários com os ids e nomes das subprefeituras
 
"""
@router.get("/subprefectures")
def get_subprefectures(db: Session = Depends(get_db)):
    return {"subprefeituras": get_all_subprefectures(db)}
