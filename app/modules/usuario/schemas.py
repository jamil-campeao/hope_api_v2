from pydantic import BaseModel
from datetime import datetime
from typing import List

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: bool

class UsuarioUpdate(BaseModel):
    nome: str
    ativo: bool

class UsuarioUpdateEmail(BaseModel):
    email_antigo: str
    email_novo: str
    codigo: str

class UsuarioUpdateSenha(BaseModel):
    senha_atual: str
    senha_nova: str
    codigo: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    data_cadastro: datetime | None = None
    data_atualizacao: datetime | None = None
    data_exclusao: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class UsuarioResponseList(BaseModel):
    usuarios: List[UsuarioResponse]
