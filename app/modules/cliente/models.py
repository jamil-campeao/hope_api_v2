from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, MetaData, ForeignKey, Boolean
from app.core.database import Base




class Cliente(Base):
    __tablename__ = "clientes"
    # Opcional se metadata já define schema, mas boa prática para clareza
    __table_args__ = {'schema': 'cliente'}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    usuario_cadastro = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=False)
    usuario_ultima_atualizacao = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=True)
    usuario_exclusao = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=True)
    data_cadastro = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    data_exclusao = Column(DateTime(timezone=True), nullable=True)
