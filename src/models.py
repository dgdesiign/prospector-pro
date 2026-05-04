from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String, unique=True)
    site = Column(String)
    rating = Column(Float)
    user_ratings_total = Column(Integer)
    price_level = Column(Integer)
    cnpj = Column(String)
    razao_social = Column(String)
    atividade_principal = Column(String)
    email = Column(String)
    tier = Column(String)
