from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import get_floods_this_month, get_floods_by_subprefecture, get_all_floods, get_floods_by_specific_subprefecture, get_floods_previous_month
from app.database import get_db
router = APIRouter()

"""
_summary_
cria uma rota para retornar o total de enchentes no último mês

_parameters_
db: Session = Depends(get_db) -> sessão do banco de dados

_returns_

_total_: total de enchentes no último mês
 
"""
@router.get("/floods/this-month")
def this_month_floods(db: Session = Depends(get_db)):
    return {"total": get_floods_this_month(db)}

"""
_summary_
Rota para retornar o total de enchentes no mês anterior ao último mês

_parameters_
db: Session = Depends(get_db) -> sessão do banco de dados
    
_returns_
_total_: total de enchentes no mês anterior ao último mês
    
"""
@router.get("/floods/previous-month")
def floods_previous_month (db: Session = Depends(get_db)):
    return {"total": get_floods_previous_month (db)}

"""
_summary_
Rota para retornar o total de enchentes por subprefeitura

_parameters_
db: Session = Depends(get_db) -> sessão do banco de dados

Returns:
_subprefecture_: _count_

"""
@router.get("/floods/by-subprefecture")
def floods_by_subprefecture(db: Session = Depends(get_db)):
    return get_floods_by_subprefecture(db)

"""
_summary_
Rota para retornar todas as enchentes

_parameters_
db: Session = Depends(get_db) -> sessão do banco de dados

Returns:
_floods_: lista de enchentes
"""
@router.get("/floods/all")
def all_floods(db: Session = Depends(get_db)):
    return {"floods": get_all_floods(db)}

"""
_summary_
Rota para retornar o total de enchentes por subprefeitura

_parameters_
subprefecture: str -> nome da subprefeitura
db: Session = Depends(get_db) -> sessão do banco de dados

Returns:
_subprefecture_: _count_

"""
@router.get("/floods/{subprefecture}")
def floods_by_specif_subprefecture(subprefecture: str, db: Session = Depends(get_db)):
    floods = get_floods_by_specific_subprefecture(db, subprefecture)
    if not floods:
        return {"message": f"Nenhum dado encontrado para a subprefeitura {subprefecture}"}
    return {"subprefecture": subprefecture, "floods": floods}

