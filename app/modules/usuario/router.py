from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.usuario import schemas
from app.modules.usuario import service
from app.modules.usuario.models import Usuario

router = APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
)

@router.post(
    "",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo usuário"
)
async def criar_novo_usuario(
    usuario_in: schemas.UsuarioCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.UsuarioResponse:
    usuario = await service.criar_usuario(db=db, usuario_in=usuario_in)
    return schemas.UsuarioResponse.model_validate(usuario)

@router.get("/{id}", response_model=schemas.UsuarioResponse, status_code=status.HTTP_200_OK, summary="Buscar um usuário pelo ID")
async def get_usuario_by_id(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.UsuarioResponse:
    usuario = await service.get_usuario_by_id(db=db, id=id)
    return schemas.UsuarioResponse.model_validate(usuario)

# @router.get("/", response_model=schemas.UsuarioResponseList, status_code=status.HTTP_200_OK, summary="Buscar todos os usuários")
# async def get_all_usuarios(
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.UsuarioResponseList:
#     return await service.get_all_usuarios(db=db)
