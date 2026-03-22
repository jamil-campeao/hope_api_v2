from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.modules.usuario.models import Usuario, Sessao
from app.modules.auth import schemas

from datetime import datetime, timedelta
import jwt
from app.core.security import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    """
    Login compatível com OAuth2 para receber os Tokens de Acesso e de Renovação (Refresh Token).
    """
    result = await db.execute(select(Usuario).where(Usuario.email == form_data.username))
    user = result.scalars().first()

    if not user or not user.senha or not verify_password(form_data.password, user.senha):
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
    if not user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")

    refresh = create_refresh_token(subject=user.id)
    nova_sessao = Sessao(
        usuario_id=user.id,
        refresh_token=refresh,
        expira_em=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(nova_sessao)
    await db.commit()

    return {
        "access_token": create_access_token(subject=user.id),
        "refresh_token": refresh,
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    body: schemas.RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    """
    Renova o Access Token por mais tempo informando um Refresh Token previamente gerado e válido.
    """
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido para renovação")

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token corrompido")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Refresh Token expirado ou formato inválido")

    # Validar a Sessão física no banco de dados
    result = await db.execute(select(Sessao).where(Sessao.refresh_token == body.refresh_token))
    sessao = result.scalars().first()

    if not sessao or not sessao.expira_em or sessao.expira_em < datetime.utcnow():
        if sessao:
            await db.delete(sessao)
            await db.commit()
        raise HTTPException(status_code=401, detail="Sessão revogada ou expirada")

    # Validar se o usuário que enviou o token de fato ainda existe e está ativo no sistema
    user_result = await db.execute(select(Usuario).where(Usuario.id == sessao.usuario_id))
    user = user_result.scalars().first()

    if not user or not user.ativo:
        raise HTTPException(status_code=401, detail="Usuário bloqueado ou inexistente")

    # Rotacionar o Token de Refresh (Deleta o antigo, entrega um zero km)
    await db.delete(sessao)

    new_refresh = create_refresh_token(subject=user.id)
    nova_sessao = Sessao(
        usuario_id=user.id,
        refresh_token=new_refresh,
        expira_em=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(nova_sessao)
    await db.commit()

    return {
        "access_token": create_access_token(subject=user.id),
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }
