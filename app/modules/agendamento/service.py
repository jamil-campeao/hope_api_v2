from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.modules.agendamento.models import Reserva
from app.modules.agendamento.schemas import ReservaCreate, ReservaResponseList, ReservaUpdate
from app.core.config import settings

# Você poderia injetar um client HTTP aqui (ex: httpx.AsyncClient) para testes mais fáceis.
import httpx

async def verificar_conflito_horario(
    db: AsyncSession, data_inicio: datetime, data_fim: datetime, exclude_id: int | None = None
) -> bool:
    """Verifica se existe conflito de horário para novas reservas."""

    conditions = [
        Reserva.status != "cancelado",
        or_(
            # A nova reserva começa durante uma reserva existente
            and_(Reserva.data_inicio <= data_inicio, Reserva.data_fim > data_inicio),
            # A nova reserva termina durante uma reserva existente
            and_(Reserva.data_inicio < data_fim, Reserva.data_fim >= data_fim),
            # A nova reserva engloba uma reserva existente
            and_(Reserva.data_inicio >= data_inicio, Reserva.data_fim <= data_fim),
        )
    ]

    if exclude_id is not None:
        conditions.append(Reserva.id != exclude_id)

    query = select(Reserva).where(and_(*conditions))

    result = await db.execute(query)
    conflito = result.scalars().first()
    return conflito is not None

async def reserva_validacoes(
    db: AsyncSession,
    id: int | None = None,
    reserva_in: ReservaCreate | ReservaUpdate | None = None
) -> Reserva | None:
    reserva = None
    if id is not None:
        # Pega a reserva do banco, se não existir o get_reserva_by_id já lança 404
        reserva = await get_reserva_by_id(db, id)

        if reserva.status == 'cancelado':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reserva já cancelada."
            )

    if reserva_in:
        if reserva_in.data_fim <= reserva_in.data_inicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de fim deve ser posterior à data de início."
            )

        # Trata o caso de atualização onde não queremos dar conflito com a própria reserva sendo atualizada
        tem_conflito = await verificar_conflito_horario(
            db, reserva_in.data_inicio, reserva_in.data_fim, exclude_id=id
        )

        if tem_conflito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflito de horário. Já existe uma reserva neste período."
            )

    return reserva


async def notificar_n8n(reserva: Reserva) -> None:
    """
    Placeholder para chamada de webhook no n8n.
    Integrações de WhatsApp (via WAHA) ou Google Calendar.
    """
    webhook_url = settings.N8N_WEBHOOK_URL
    if not webhook_url:
        return

    payload = {
        "event": "nova_reserva",
        "data": {
            "reserva_id": reserva.id,
            "cliente_id": reserva.cliente_id,
            "data_inicio": reserva.data_inicio.isoformat() if reserva.data_inicio else None,
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(webhook_url, json=payload, timeout=5.0)
    except Exception as e:
        # Fazer logging de erro, mas não quebrar o fluxo do usuário (reserva já salva)
        print(f"Erro ao notificar n8n: {e}")


async def criar_reserva(db: AsyncSession, reserva_in: ReservaCreate, usuario_id: int) -> Reserva:
    """
    Cria uma nova reserva após verificar regras de negócio (conflitos de hora).
    """
    await reserva_validacoes(db=db, reserva_in=reserva_in)

    nova_reserva = Reserva(
        empresa_id=reserva_in.empresa_id,
        cliente_id=reserva_in.cliente_id,
        servico_id=reserva_in.servico_id,
        data_inicio=reserva_in.data_inicio,
        data_fim=reserva_in.data_fim,
        status="pendente",
        usuario_criacao=usuario_id,
    )

    db.add(nova_reserva)
    await db.commit()
    await db.refresh(nova_reserva)

    # Após o commit com sucesso, aciona integrações assíncronas via Webhook
    await notificar_n8n(nova_reserva)

    return nova_reserva


async def get_all_reservas(db: AsyncSession) -> ReservaResponseList:
    result = await db.execute(select(Reserva))
    reservas = result.scalars().all()

    return ReservaResponseList(reservas=list(reservas))


async def get_reserva_by_id(db: AsyncSession, id: int) -> Reserva:
    result = await db.execute(select(Reserva).where(Reserva.id == id))
    reserva = result.scalars().first()

    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada."
        )

    return reserva

async def cancela_reserva_by_id(db: AsyncSession, id: int, usuario_id: int) -> Reserva:
    reserva = await reserva_validacoes(db=db, id=id)
    assert reserva is not None

    reserva.status = "cancelado"
    reserva.usuario_exclusao = usuario_id
    await db.commit()
    return reserva

async def atualiza_reserva_by_id(db: AsyncSession, id: int, reserva_in: ReservaUpdate, usuario_id: int) -> Reserva:
    reserva = await reserva_validacoes(db=db, id=id, reserva_in=reserva_in)
    assert reserva is not None

    reserva.servico_id = reserva_in.servico_id
    reserva.data_inicio = reserva_in.data_inicio
    reserva.data_fim = reserva_in.data_fim
    reserva.status = reserva_in.status
    reserva.usuario_ultima_atualizacao = usuario_id

    await db.commit()
    await db.refresh(reserva)
    return reserva
