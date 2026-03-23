from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.modules.empresa.models import Empresa
from app.modules.empresa.schemas import EmpresaCreate, EmpresaResponseList, EmpresaUpdate
from app.core.config import settings
from app.utils.validacoes.documento import valida_documento
from app.utils.formatacao.telefone import formatar_telefone
from app.utils.validacoes.email import valida_email


async def empresa_validacoes(db: AsyncSession, empresa_in: EmpresaCreate | EmpresaUpdate, id: int | None = None):
    #Valido se o ID da empresa existe se id for passado
    if id:
        empresa = await get_empresa_by_id(db, id)
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada"
            )

    if empresa_in.documento_cnpj and empresa_in.documento_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informado documento CNPJ e CPF, favor informar apenas um."
        )

    if not empresa_in.documento_cnpj and not empresa_in.documento_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF ou CNPJ deve ser informado."
        )

    if empresa_in.documento_cnpj or empresa_in.documento_cpf:
        #Valido se o documento é valido
        documento = empresa_in.documento_cnpj or empresa_in.documento_cpf
        if not valida_documento(documento):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Documento inválido"
            )

        # Valido se o documento já existe
        condicoes = []
        if empresa_in.documento_cnpj:
            condicoes.append(Empresa.documento_cnpj == empresa_in.documento_cnpj)
        if empresa_in.documento_cpf:
            condicoes.append(Empresa.documento_cpf == empresa_in.documento_cpf)
            
        stmt = select(Empresa).where(or_(*condicoes))
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Documento já cadastrado"
            )

    # Validações Email
    if empresa_in.email is not None:
        # Valido se o email é valido primeiro para barrar strings vazias
        if not valida_email(empresa_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email inválido"
            )
            
        # Valido se o email já existe
        stmt = select(Empresa).where(Empresa.email == empresa_in.email)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )



async def criar_empresa(db: AsyncSession, empresa_in: EmpresaCreate) -> Empresa:
    try:
        await empresa_validacoes(db=db, empresa_in=empresa_in)
        empresa_in.telefone = formatar_telefone(empresa_in.telefone)
        empresa = Empresa(**empresa_in.model_dump())
        db.add(empresa)
        await db.commit()
        await db.refresh(empresa)
    except HTTPException as he:
        await db.rollback()
        raise he
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return empresa

async def get_empresa_by_id(db: AsyncSession, id: int) -> Empresa:
    result = await db.execute(select(Empresa).where(Empresa.id == id))
    empresa = result.scalar_one_or_none()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    return empresa

async def update_empresa(db: AsyncSession, id: int, empresa_in: EmpresaUpdate) -> Empresa:
    try:
        await empresa_validacoes(db=db, empresa_in=empresa_in, id=id)
        empresa.razao_social = empresa_in.razao_social
        empresa.nome_fantasia = empresa_in.nome_fantasia
        empresa.email = empresa_in.email
        empresa.telefone = formatar_telefone(empresa_in.telefone)
        empresa.documento_cpf = empresa_in.documento_cpf
        empresa.documento_cnpj = empresa_in.documento_cnpj
        empresa.ativo = empresa_in.ativo
        await db.commit()
        await db.refresh(empresa)
    except HTTPException as he:
        await db.rollback()
        raise he
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return empresa

async def delete_empresa(db: AsyncSession, id: int) -> None:
    try:
        empresa = await get_empresa_by_id(db, id)

        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada"
            )

        if empresa.ativo == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empresa já inativa"
            )

        empresa.ativo = False
        empresa.data_exclusao = datetime.now()
        await db.commit()
    except HTTPException as he:
        await db.rollback()
        raise he
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
