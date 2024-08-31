from utils import db
from models.usuario import Usuario
from ChomikBox import Chomik

## Consultas

# Buscar usuário
def get_usuario(username):
    with db.Session() as session:
        return session.query(Usuario).filter_by(username=username).first()

## Operacoes
# Adicionar
def add_usuario(user):
    with db.Session() as session:
        existente = get_usuario(username=user.username)
        
        if existente is not None:
            existente.Chomik = Chomik(existente.username, existente.password)
            return existente

        session.add(user)
        session.commit()
        print(user.id)
        return user

# Deletar
def delete_usuario(user):
    with db.Session() as session:
        existente = get_usuario(username=user.username)
        
        if existente is None:
            raise Exception("Usuário não existe")
        
        session.delete(user)
        session.commit()

# Atualizar
def atualizar_usuario(user):
    with db.Session() as session:
        existente = get_usuario(username=user.username)
        
        if existente is None:
            raise Exception("Usuário não existe")
        
        existente.username = user.username
        existente.password = user.password
        session.commit()