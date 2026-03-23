from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, MetaData, Boolean
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    # Opcional se metadata já define schema, mas boa prática para clareza
    __table_args__ = {'schema': 'empresa'}

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    documento_cpf = Column(String, nullable=True, unique=True)
    documento_cnpj = Column(String, nullable=True, unique=True)
    ativo = Column(Boolean, default=True, nullable=False)
    data_cadastro = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    data_exclusao = Column(DateTime(timezone=True), nullable=True)
