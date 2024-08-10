from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models.usuario import Base as userBase
from models.pasta import Base as pastaBase
from models.arquivo import Base as arquivoBase

# DB
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Sessão
Session = sessionmaker(bind=engine, expire_on_commit=False)

def iniciar_db():
    # Criar tabelas
    userBase.metadata.create_all(engine)
    pastaBase.metadata.create_all(engine)
    arquivoBase.metadata.create_all(engine)

if __name__ == "__main__":
    iniciar_db()