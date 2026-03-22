from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, MetaData, ForeignKey
from app.core.database import Base



class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'usuario'}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    data_cadastro = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    data_exclusao = Column(DateTime(timezone=True), nullable=True)

class Sessao(Base):
    __tablename__ = "sessoes"
    __table_args__ = {'schema': 'usuario'}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=False, index=True)
    refresh_token = Column(String, nullable=False, unique=True, index=True)
    expira_em = Column(DateTime(timezone=True), nullable=False)
    criado_em = Column(DateTime(timezone=True), default=datetime.utcnow)
