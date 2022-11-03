# Teste das funcionalidades do pyChomikBox
from models.usuario import Usuario
from models.usuario import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# TODO Melhorar a escrita do arquivo salvo e dar uma olhada no folder cache do chomikbox para ver o que é.
if __name__ == '__main__':
    # DB
    engine = create_engine('sqlite:///../../db.sqlite3', echo=True)

    # Sessão
    with Session(engine) as session:
        Base.metadata.create_all(engine)

        user = Usuario(username="João")

        session.add(user)
        session.commit()
