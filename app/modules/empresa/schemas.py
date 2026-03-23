from datetime import datetime
from pydantic import BaseModel, Field

class EmpresaCreate(BaseModel):
    razao_social: str = Field(..., description="Razão social da empresa")
    nome_fantasia: str = Field(..., description="Nome fantasia da empresa")
    email: str = Field(..., description="Email da empresa")
    telefone: str = Field(..., description="Telefone da empresa")
    documento_cnpj: str | None = Field(None, description="Documento CNPJ da empresa")
    documento_cpf: str | None = Field(None, description="Documento CPF da empresa")
    ativo: bool = Field(..., description="Status da empresa")

class EmpresaUpdate(BaseModel):
    razao_social: str = Field(..., description="Razão social da empresa")
    nome_fantasia: str = Field(..., description="Nome fantasia da empresa")
    email: str = Field(..., description="Email da empresa")
    telefone: str = Field(..., description="Telefone da empresa")
    documento_cnpj: str | None = Field(None, description="Documento CNPJ da empresa")
    documento_cpf: str | None = Field(None, description="Documento CPF da empresa")
    ativo: bool = Field(..., description="Status da empresa")

class EmpresaResponse(BaseModel):
    id: int
    razao_social: str
    nome_fantasia: str
    email: str
    telefone: str
    ativo: bool
    documento_cnpj: str | None = None
    documento_cpf: str | None = None
    data_cadastro: datetime
    data_atualizacao: datetime | None = None
    data_exclusao: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class EmpresaResponseList(BaseModel):
    empresas: list[EmpresaResponse]