from fastapi import FastAPI, Query
from enum import Enum
from typing import Union
from pydantic import BaseModel

app = FastAPI()


@app.get("/") #decorador do get relacionado ao endpoint "/"
async def root(): #função assíncrona
    return {"message": "Hello"}

@app.post("/criar")
async def root():
    return {"message": "POST criado"}

@app.get("/items/{item_id}") #{item_id} é a variável de rota
async def read_item(item_id: int):
    print("item_id: ", item_id)
    print("type(item_id): ", type(item_id))
    return {"item_id": item_id}

class BRStates(str, Enum):
    sp = "1"
    rj = "2"
    mg = "3"
    es = "4"
    
@app.get("/states/{state_id}")
async def read_state(state_id: BRStates):
    if state_id.value == "1":
        return {"São Paulo"}
    if state_id.value == "2":
        return {"Rio de Janeiro"}
    if state_id.value == "3":
        return {"Minas Gerais"}
    if state_id.value == "4":
        return {"Espírito Santo"}
    

    
fake_items_db = [{"item_name": "01"}, 
                 {"item_name": "02"}, 
                 {"item_name": "03"},
                 {"item_name": "04"},
                 {"item_name": "05"},
                 {"item_name": "06"},
                 {"item_name": "07"},
                 {"item_name": "08"},
                 {"item_name": "09"},
                 {"item_name": "10"},]


@app.get("/fake_db/")
async def read_item(skip: int = 0, limit: int = 5):
    return fake_items_db[skip : skip + limit]

@app.get("/item_name/")
async def item_name(name: str, age: int | None = None, angry: bool = False):
    if age is not None:
        msg = f"My name is {name} and I am {age} years old!"
        return {"message" : msg}
    if angry is not None:
        msg = f"My name is {name} and I am NOT happy :()"
        return {"message" : msg}
    msg = f"My name is {name} and I am happy"
    return {"message" : msg}

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    
@app.post('/items/')
async def create_item(item : Item):
    print(item)
    print(item.model_dump())
    return item

class Curso(BaseModel):
    name : str
    duration : int

@app.put('/curso/{curso_id}')
async def update_curso(curso_id: int, curso: Curso):
    return {"curso_id" : curso_id, **curso.model_dump()}

@app.get("/item/")
async def read_items(
        q: Union[str, None] = Query(
            default=None, 
            max_length=50, 
            min_length=10
        )
    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results