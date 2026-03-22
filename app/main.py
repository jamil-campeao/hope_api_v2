from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base
from app.modules.agendamento import models as agendamento_models
from app.modules.agendamento.router import router as agendamento_router

from app.modules.usuario import models as usuario_models
from app.modules.usuario.router import router as usuario_router

from app.modules.cliente import models as cliente_models
from app.modules.cliente.router import router as cliente_router

from app.modules.empresa import models as empresa_models
from app.modules.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI): # type: ignore
    """
    Lifespan da aplicação:
    Cria os schemas e tabelas na inicialização se não existirem (apenas no bootstrap).
    Para produção recomenda-se migrações com Alembic.
    """
    async with engine.begin() as conn:
        from sqlalchemy import text

        # Cria os schemas do projeto
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS agendamento;"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS usuario;"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS cliente;"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS empresa;"))

        # Sincroniza todas as tabelas de uma só vez (todas registradas na Base global)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Liberação de recursos
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Inclusão dos módulos (Monólito Modular)
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(cliente_router)
app.include_router(agendamento_router)

@app.get("/health", tags=["Health"], response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Endpoint de health check."""
    return {"status": "ok", "message": "Hope API rodando com sucesso."}
