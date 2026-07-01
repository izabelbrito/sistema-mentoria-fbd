from sqlalchemy import Column, Integer, String
from database import Base

class Disciplina(Base):
    __tablename__ = "disciplina"

    id_disciplina = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    carga_horaria = Column(Integer, nullable=False)

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False) # <- Linha adicionada
    email = Column(String(100), unique=True, nullable=False)