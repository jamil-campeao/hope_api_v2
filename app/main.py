from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine
from app.modules.agendamento import models as agendamento_models
from app.modules.agendamento.router import router as agendamento_router

@asynccontextmanager
async def lifespan(app: FastAPI): # type: ignore
    """
    Lifespan da aplicação:
    Cria os schemas e tabelas na inicialização se não existirem (apenas no bootstrap).
    Para produção recomenda-se migrações com Alembic.
    """
    async with engine.begin() as conn:
        from sqlalchemy import text
        
        # Cria o schema 'agendamento' 
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS agendamento;"))
        # Sincroniza as tabelas
        await conn.run_sync(agendamento_models.Base.metadata.create_all)
    
    yield
    
    # Liberação de recursos
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Inclusão dos módulos (Monólito Modular)
app.include_router(agendamento_router)

@app.get("/health", tags=["Health"], response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Endpoint de health check."""
    return {"status": "ok", "message": "Hope API rodando com sucesso."}
