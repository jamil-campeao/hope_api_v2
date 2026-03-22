from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.cliente import schemas
from app.modules.cliente import service


router = APIRouter(
    prefix="/cliente",
    tags=["Clientes"]
)
