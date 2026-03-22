from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.usuario.models import Usuario
from app.modules.agendamento import schemas
from app.modules.agendamento import service

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)

@router.post(
    "",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo agendamento",
    dependencies=[Depends(get_current_user)],
)
async def criar_novo_agendamento(
    reserva_in: schemas.ReservaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> schemas.ReservaResponse:
    assert current_user.id is not None
    reserva = await service.criar_reserva(db=db, reserva_in=reserva_in, usuario_id=current_user.id)
    return schemas.ReservaResponse.model_validate(reserva)

@router.get("/all",
response_model=schemas.ReservaResponseList,
status_code=status.HTTP_200_OK,
summary="Lista todas as reservas",
dependencies=[Depends(get_current_user)],
)
async def get_all_reservas(
    db: AsyncSession = Depends(get_db)
) -> schemas.ReservaResponseList:
    return await service.get_all_reservas(db=db)

@router.get(
    "/{id}",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca uma reserva pelo ID",
    dependencies=[Depends(get_current_user)],
    )
async def get_reserva_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    reserva = await service.get_reserva_by_id(db=db, id=id)
    return schemas.ReservaResponse.model_validate(reserva)

@router.delete(
    "/{id}",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Deleta uma reserva pelo ID",
    dependencies=[Depends(get_current_user)],
    )
async def cancela_reserva_by_id(
    id: int,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    assert current_user.id is not None
    reserva = await service.cancela_reserva_by_id(db=db, id=id, usuario_id=current_user.id)
    return schemas.ReservaResponse.model_validate(reserva)

@router.put(
    "/{id}",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma reserva pelo ID",
    dependencies=[Depends(get_current_user)],
    )
async def atualiza_reserva_by_id(
    id: int,
    reserva_in: schemas.ReservaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.ReservaResponse:
    assert current_user.id is not None
    reserva = await service.atualiza_reserva_by_id(db=db, id=id, reserva_in=reserva_in, usuario_id=current_user.id)
    return schemas.ReservaResponse.model_validate(reserva)
