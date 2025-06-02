from typing import Optional
from pydantic import BaseModel as SCBaseModel

class ProfissaoSchemas(SCBaseModel):
    id: Optional[int] = None
    nome: str
    area: str
    formacao: str
    salario: float
    foto: str
    
    class Config:
        orm_mode = True