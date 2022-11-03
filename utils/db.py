from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Sessão
session = sessionmaker(bind=engine)

def iniciar_db(base, engine):
    # Criar tabelas
    base.metadata.create_all(engine)

def criar_engine():
    # Gerar tabelas para cada model
    from models.Chomik import Base
    iniciar_db(Base, engine)

if __name__ == '__main__':
    criar_engine()