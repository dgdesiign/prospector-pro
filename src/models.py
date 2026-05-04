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
    
    # Novos Campos de Inteligência Elite
    score = Column(Integer, default=0) # Lead Score 0-100
    status_funil = Column(String, default="Frio") # Frio, Prospecção, Qualificação, Fechamento
    risco_juridico = Column(String) # Baixo, Médio, Alto
    capital_social = Column(Float, default=0.0)
    ultima_interacao = Column(String)
