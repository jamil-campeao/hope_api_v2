from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.empresa import schemas
from app.modules.empresa import service
from app.modules.empresa.models import Empresa

router = APIRouter(
    prefix="/empresa",
    tags=["Empresas"]
)

@router.post(
    "",
    response_model=schemas.EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova empresa",
    dependencies=[Depends(get_current_user)]
) 
async def criar_nova_empresa(
    empresa_in: schemas.EmpresaCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.EmpresaResponse:
    empresa = await service.criar_empresa(db=db, empresa_in=empresa_in)
    return schemas.EmpresaResponse.model_validate(empresa)

@router.get(
    "/{id}", 
    response_model=schemas.EmpresaResponse, 
    status_code=status.HTTP_200_OK, 
    dependencies=[Depends(get_current_user)],
    summary="Buscar uma empresa pelo ID"
    )
async def get_empresa_by_id(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.EmpresaResponse:
    empresa = await service.get_empresa_by_id(db=db, id=id)
    return schemas.EmpresaResponse.model_validate(empresa)


@router.put(
    "/{id}", 
    response_model=schemas.EmpresaResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Atualizar uma empresa pelo ID",
    dependencies=[Depends(get_current_user)]
    )
async def update_empresa(
    id: int,
    empresa_in: schemas.EmpresaUpdate,
    db: AsyncSession = Depends(get_db)
) -> schemas.EmpresaResponse:
    empresa = await service.update_empresa(db=db, id=id, empresa_in=empresa_in)
    return schemas.EmpresaResponse.model_validate(empresa)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar uma empresa pelo ID",
    dependencies=[Depends(get_current_user)]
)
async def delete_empresa(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    await service.delete_empresa(db=db, id=id)

