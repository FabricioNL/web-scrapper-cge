from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime


def get_floods_this_month(db: Session):
    first_day_of_month = datetime.now().replace(day=1).strftime("%Y/%m/%d")
    first_day_of_month = (str(first_day_of_month).replace("/", "-"))
    query = text("""
        SELECT COUNT(*) FROM Alagamentos
        WHERE DATE(substr(data, 7, 4) || '-' || substr(data, 4, 2) || '-' || substr(data, 1, 2)) >= :first_day_of_month
    """)

    result = db.execute(query, {"first_day_of_month": first_day_of_month}).scalar()
    return result


def get_floods_previous_month(db: Session):
    query = text("""
        SELECT COUNT(*) FROM Alagamentos
        WHERE DATE(substr(data, 7, 4) || '-' || substr(data, 4, 2) || '-' || substr(data, 1, 2)) 
        BETWEEN DATE('now', 'start of month', '-1 month') 
            AND DATE('now', 'start of month', '-1 day')
    """)

    result = db.execute(query).scalar()
    return result


def get_all_floods(db: Session):
    query = text("""
        SELECT * 
        FROM Alagamentos 
        INNER JOIN Subprefeitura 
        ON Alagamentos.subprefeitura_id = Subprefeitura.id
    """)
    
    list_columns_name = [
        "id", "subprefeitura_id", "data", "quantidade_alagamentos", "referencia", 
        "sentido", "rua", "horario_inicio", "horario_fim", "subprefeitura_id", "nome"
    ]
    
    result = db.execute(query).fetchall()
    
    # Converte cada linha em um dicionário
    return [dict(zip(list_columns_name, row)) for row in result]


def get_all_subprefectures(db: Session):
    query = text("""
        SELECT * FROM Subprefeitura
    """)

    list_columns_name = ["id", "nome"]
    result = db.execute(query).fetchall()
    return [dict(zip(list_columns_name, row)) for row in result]


def get_floods_by_subprefecture(db: Session):
    query = text("""
        SELECT Subprefeitura.nome, COUNT(Alagamentos.id) AS total_alagamentos
        FROM Alagamentos
        INNER JOIN Subprefeitura 
        ON Alagamentos.subprefeitura_id = Subprefeitura.id
        GROUP BY Subprefeitura.nome
        ORDER BY total_alagamentos DESC
    """)

    result = db.execute(query).fetchall()
    return [{"subprefeitura": row[0], "count": row[1]} for row in result]


def get_floods_by_specific_subprefecture(db: Session, subprefecture: str):
    print(subprefecture)
    query = text("""
        SELECT *
        FROM Alagamentos
        INNER JOIN Subprefeitura 
        ON Alagamentos.subprefeitura_id = Subprefeitura.id
        WHERE Subprefeitura.nome = :subprefecture
    """)

    list_columns_name = ["id", "subprefeitura_id", "data", "quantidade_alagamentos", "referencia", "sentido", "rua", "horario_inicio", "horario_fim", "subprefeitura_id", "nome"]
    result = db.execute(query, {"subprefecture": subprefecture}).fetchall()
    return [dict(zip(list_columns_name, row)) for row in result]
