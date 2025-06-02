from core.configs import settings
from sqlalchemy import Column, Integer, String, Float

class ProfissaoModel(settings.DBBaseModel):
    __tablename__="profissao"
    
    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(256))
    area: str = Column(String(256))
    formacao: str = Column(String(256))
    salario: float = Column(Float())
    foto: str = Column(String(256))
    
    