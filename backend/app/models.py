from sqlalchemy import Column, Integer, String, Date, ForeignKey, TypeDecorator, DateTime
from app.database import Base
#from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from datetime import date, datetime

class CustomDate(TypeDecorator):
    impl = String  # Armazena a data como string no banco

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return value  # Nenhuma modificação na inserção
        elif isinstance(value, datetime.date):
            return value.strftime("%d/%m/%Y")
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                # Converte de DD/MM/YYYY para um objeto `datetime.date`
                return datetime.strptime(value, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError(f"Formato de data inválido no banco: {value}")
        return value


class Flood(Base):
    __tablename__ = "Alagamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    subprefeitura_id = Column(Integer, ForeignKey("Subprefeitura.id"))  # ForeignKey definida corretamente
    data =  Column(DateTime)  
    quantidade_alagamentos = Column(Integer)
    referencia = Column(String)
    rua = Column(String)
    horario_inicio = Column(String)
    horario_fim = Column(String)

    # Relacionamento com Subprefecture
    subprefecture = relationship("Subprefecture", back_populates="alagamentos")



class Subprefecture(Base):
    __tablename__ = "Subprefeitura"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)

    # Relacionamento inverso
    alagamentos = relationship("Flood", back_populates="subprefecture")
    
    

class FloodBase(BaseModel):
    subprefeitura_id: int
    data: date
    quantidade_alagamentos: int
    referencia: str
    rua: str
    horario_inicio: str
    horario_fim: str

    class Config:
        from_attributes = True  # Replaces orm_mode
        arbitrary_types_allowed = True  # Allows custom types like SQLAlchemy's Date


class subprefectureBase(BaseModel):
    nome: str

    class Config:
        from_attributes = True  # Replaces orm_mode
        arbitrary_types_allowed = True  # Allows custom types like SQLAlchemy's Date
        
        
class SubprefectureFloodCount(BaseModel):
    subprefeitura: str
    count: int