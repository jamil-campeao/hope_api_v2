from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.modules.usuario.models import Usuario
from app.modules.usuario.schemas import UsuarioCreate, UsuarioResponseList, UsuarioUpdate
from app.core.config import settings
from app.core.security import get_password_hash
from app.modules.empresa.service import get_empresa_by_id
from app.utils.validacoes.email import valida_email

async def usuario_validacoes(db: AsyncSession, usuario_in: UsuarioCreate | UsuarioUpdate | None = None, id: int | None = None) -> None:
    #Valida se o email já existe
    if isinstance(usuario_in, UsuarioCreate):
        if not valida_email(usuario_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email inválido"
            )
        result = await db.execute(select(Usuario).where(Usuario.email == usuario_in.email))
        usuario = result.scalars().first()
        if usuario:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado"
            )



async def criar_usuario(db: AsyncSession, usuario_in: UsuarioCreate) -> Usuario:
    try:
        await usuario_validacoes(db=db, usuario_in=usuario_in)

        novo_usuario = Usuario(
            nome=usuario_in.nome,
            email=usuario_in.email,
            senha=get_password_hash(usuario_in.senha),
            ativo=usuario_in.ativo,
            documento_cpf=usuario_in.documento_cpf if usuario_in.documento_cpf else None,
            documento_cnpj=usuario_in.documento_cnpj if usuario_in.documento_cnpj else None
        )

        db.add(novo_usuario)
        await db.commit()
        await db.refresh(novo_usuario)

        return novo_usuario
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_usuario_by_id(db: AsyncSession, id: int) -> Usuario:
    result = await db.execute(select(Usuario).where(Usuario.id == id))
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado."
        )

    return usuario


async def vinculo_empresa_usuario(db: AsyncSession, id: int, empresa_id: int) -> Usuario:
    try:
        usuario = await get_usuario_by_id(db=db, id=id)
        empresa = await get_empresa_by_id(db=db, id=empresa_id)
        usuario.empresa_id = empresa.id
        await db.commit()
        await db.refresh(usuario)
        return usuario
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_all_usuarios(db: AsyncSession, empresa_id: int) -> UsuarioResponseList:
    try:
        result = await db.execute(select(Usuario).where(Usuario.empresa_id == empresa_id))
        usuarios = result.scalars().all()
        return UsuarioResponseList(usuarios=usuarios)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )