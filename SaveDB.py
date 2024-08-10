# Teste SQLAlchemy
from models.Chomik import Chomik, Base
from models.ChomikFolder import ChomikFolder
from utils.db import iniciar_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


if __name__ == '__main__':
    # DB
    engine = create_engine('sqlite:///db.sqlite3', echo=True)

    # Sessão
    with Session(engine) as session:
        Base.metadata.create_all(engine)

        user = Chomik('super-secret-user', 'super-secret-password')

        session.add(user)
        session.commit()

    print(user)