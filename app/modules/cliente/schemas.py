from pydantic import BaseModel
from datetime import datetime


class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str
    ativo: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    ativo: str
    usuario_cadastro: int
    usuario_cadastro_nome: str
    usuario_ultima_atualizacao: int | None = None
    usuario_ultima_atualizacao_nome: str | None = None
    usuario_exclusao: int | None = None
    usuario_exclusao_nome: str | None = None
    data_cadastro: datetime
    data_atualizacao: datetime | None = None
    data_exclusao: datetime | None = None
