from datetime import datetime, timedelta
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# JWT Setup
# Em produção, você deve definir SECRET_KEY no seu arquivo .env
SECRET_KEY = getattr(settings, "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Algoritmo de Hashing padrão (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara uma senha limpa com o Hash guardado no banco."""
    return bool(pwd_context.verify(plain_password, hashed_password))

def get_password_hash(password: str) -> str:
    """Transforma a senha em um Hash irreversível do bcrypt."""
    return str(pwd_context.hash(password))

def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    """Cria o JWT de Acesso curto."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adicionamos "type" para diferenciar tokens no backend caso necessário
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)

def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    """Cria o JWT de Renovação longo."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Any:
    """Extrai, valida o JWT e retorna o Usuário logado que fez a requisição."""
    # O import do model fica aqui dentro ou no topo (evita circular imports, mas como app.core.security não importa nada do domínio, é seguro fazer no topo, porém aqui previne problemas se módulos usarem security cedo).
    from app.modules.usuario.models import Usuario

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    result = await db.execute(select(Usuario).where(Usuario.id == int(user_id)))
    user = result.scalars().first()

    if user is None or not user.ativo:
        raise credentials_exception

    return user
