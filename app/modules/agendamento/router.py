from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.agendamento import schemas
from app.modules.agendamento import service

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)

@router.post(
    "/",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo agendamento"
)
async def criar_novo_agendamento(
    reserva_in: schemas.ReservaCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.ReservaResponse:
    return await service.criar_reserva(db=db, reserva_in=reserva_in)

@router.get("/all", response_model=schemas.ReservaResponseList, status_code=status.HTTP_200_OK, summary="Lista todas as reservas")
async def get_all_reservas(
    db: AsyncSession = Depends(get_db)
) -> schemas.ReservaResponseList:
    return await service.get_all_reservas(db=db)

@router.get("/{id}", response_model=schemas.ReservaResponse, status_code=status.HTTP_200_OK, summary="Busca uma reserva pelo ID")
async def get_reserva_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    return await service.get_reserva_by_id(db=db, id=id)

@router.delete("/{id}", response_model=schemas.ReservaResponse, status_code=status.HTTP_200_OK, summary="Deleta uma reserva pelo ID")
async def cancela_reserva_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    return await service.cancela_reserva_by_id(db=db, id=id)

@router.put("/{id}", response_model=schemas.ReservaResponse, status_code=status.HTTP_200_OK, summary="Atualiza uma reserva pelo ID")
async def atualiza_reserva_by_id(
    id: int,
    reserva_in: schemas.ReservaUpdate,
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    return await service.atualiza_reserva_by_id(db=db, id=id, reserva_in=reserva_in)