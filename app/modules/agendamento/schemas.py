from datetime import datetime
from pydantic import BaseModel, Field

class ReservaCreate(BaseModel):
    empresa_id: int = Field(..., gt=0, description="ID da empresa (barbearia)")
    cliente_id: int = Field(..., gt=0, description="ID do cliente")
    servico_id: int = Field(..., gt=0, description="ID do serviço agendado")
    data_inicio: datetime = Field(..., description="Data e hora do início do agendamento")
    data_fim: datetime = Field(..., description="Data e hora do fim do agendamento")

    # Podem haver validações com model_validator para garantir data_fim > data_inicio

class ReservaUpdate(BaseModel):
    servico_id: int = Field(..., gt=0, description="ID do serviço agendado")
    data_inicio: datetime = Field(..., description="Data e hora do início do agendamento")
    data_fim: datetime = Field(..., description="Data e hora do fim do agendamento")
    status: str = Field(..., description="Status da reserva")

class ReservaResponse(BaseModel):
    id: int
    empresa_id: int
    cliente_id: int
    servico_id: int
    data_inicio: datetime
    data_fim: datetime
    status: str
    criado_em: datetime
    atualizado_em: datetime | None = None

    model_config = {
        "from_attributes": True # Para ORM mode com SQLAlchemy 2.0
    }

class ReservaResponseList(BaseModel):
    reservas: list[ReservaResponse]
