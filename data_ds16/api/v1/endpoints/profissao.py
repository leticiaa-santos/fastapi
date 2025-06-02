from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.profissao_model import ProfissaoModel
from schemas.profissao_schemas import ProfissaoSchemas
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProfissaoSchemas)
async def post_profissao(profissao: ProfissaoSchemas, db: AsyncSession = Depends(get_session)):
    nova_profissao = ProfissaoModel(nome=profissao.nome,
                                    area=profissao.area,
                                    formacao=profissao.formacao,
                                    salario=profissao.salario,
                                    foto=profissao.foto)
    
    db.add(nova_profissao)
    await db.commit()
    
    return nova_profissao

@router.get("/", response_model=List[ProfissaoSchemas])
async def get_profissoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel)
        result = await session.execute(query)
        profissoes: List[ProfissaoModel] = result.scalars().all()
        
        return profissoes
    
@router.get("/{profissao_id}", response_model=ProfissaoSchemas)
async def get_profissao(profissao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao = result.scalar_one_or_none()
        
        if profissao:
            return profissao
        else:
            raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)
        
@router.put("/{profissao_id}", response_model=ProfissaoSchemas, status_code=status.HTTP_202_ACCEPTED)
async def put_profissao(profissao_id: int, profissao: ProfissaoSchemas, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao_up = result.scalar_one_or_none()
        
        if profissao_up:
            profissao_up.nome = profissao.nome
            profissao_up.area = profissao.area
            profissao_up.formacao = profissao.formacao
            profissao_up.salario = profissao.salario
            profissao_up.foto = profissao.foto
            
            await session.commit()
            return profissao_up
        else:
            raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete("/{profissao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profissao(profissao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao_del = result.scalar_one_or_none()
        
        if profissao_del:
            await session.delete(profissao_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)