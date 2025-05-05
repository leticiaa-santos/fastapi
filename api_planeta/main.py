from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

planetas = {
    1: {"name": "Mercúrio", "qtd_luas": 0, "clima": "temperaturas elevadas"},
    2: {"name": "Vênus", "qtd_luas": 0, "clima": "temperaturas extremamente altas e atmosfera densa"},
    3: {"name": "Terra", "qtd_luas": 1, "clima": "variado, com zonas temperadas, frias e quentes"},
    4: {"name": "Marte", "qtd_luas": 2, "clima": "clima frio e árido"},
    5: {"name": "Júpiter", "qtd_luas": 79, "clima": "atmósfera de gás e tempestades constantes"},
    6: {"name": "Saturno", "qtd_luas": 83, "clima": "atmósfera de hidrogênio e hélio, com anéis"},
    7: {"name": "Urano", "qtd_luas": 27, "clima": "temperaturas extremamente baixas, atmosfera de hidrogênio"},
    8: {"name": "Netuno", "qtd_luas": 14, "clima": "clima frio e ventos fortes, atmosfera de hidrogênio e hélio"},
}

class Planeta(BaseModel):
    name: str
    qtd_luas: int
    clima: str | None = None

@app.get("/planetas/")
async def listar_planetas():
    return planetas

@app.get("/planetas/{planeta_id}/")
async def ver_planeta(planeta_id: int):
    if planeta_id not in planetas:
        return {"mensagem": "Planeta não encontrado"}
    return planetas[planeta_id]

@app.post("/criar/")
async def criar_planeta(planeta: Planeta):
    return planeta

@app.put("/atualizar/{planeta_id}/")
async def atualizar_planeta(planeta_id: int, planeta: Planeta):
    atualizado = {"planeta_id": planeta_id, "planeta": planeta}
    return atualizado
    