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
    ativo = Column(Boolean, default=True, nullable=False)
    usuario_cadastro = Column(Integer, nullable=False)
    usuario_ultima_atualizacao = Column(Integer, nullable=True)
    usuario_exclusao = Column(Integer, nullable=True)
    data_cadastro = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    data_exclusao = Column(DateTime(timezone=True), nullable=True)
