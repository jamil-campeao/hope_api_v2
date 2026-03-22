from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, MetaData, ForeignKey
from app.core.database import Base



class Reserva(Base):
    __tablename__ = "reservas"
    # Opcional se metadata já define schema, mas boa prática para clareza
    __table_args__ = {'schema': 'agendamento'}

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False, index=True)
    servico_id = Column(Integer, nullable=False)
    data_inicio = Column(DateTime(timezone=True), nullable=False, index=True)
    data_fim = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pendente") # pendente, confirmado, cancelado
    usuario_criacao = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=False)
    usuario_ultima_atualizacao = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=True)
    usuario_exclusao = Column(Integer, ForeignKey("usuario.usuarios.id"), nullable=True)
    criado_em = Column(DateTime(timezone=True), default=datetime.utcnow)
    atualizado_em = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    empresa_id = Column(Integer, nullable=False, index=True)
