from utils import db
from models.arquivo import Arquivo
import json

## Consultas

# Buscar arquivo
def get_arquivo(arquivo_id):
    with db.Session() as session:
        return session.query(Arquivo).filter_by(arquivo_id=arquivo_id).first()

# Buscar arquivos
def get_all_arquivos():
    with db.Session() as session:
        return session.query(Arquivo).all()

def get_all_arquivos_json():
    with db.Session() as session:
        list = session.query(Arquivo).all()
        return json.dumps([x.as_dict() for x in list])

## Operacoes
# Adicionar
def add_arquivo(arquivo):
    with db.Session() as session:
        existente = get_arquivo(arquivo_id=arquivo.arquivo_id)
        
        if existente is not None:
            return existente

        session.add(arquivo)
        session.commit()
        return get_arquivo(arquivo_id=arquivo.arquivo_id)

# # Deletar
# def delete_usuario(user):
#     with db.Session() as session:
#         existente = get_usuario(username=user.username)
        
#         if existente is None:
#             raise Exception("Usuário não existe")
        
#         session.delete(user)
#         session.commit()

def delete_all_arquivos():
    with db.Session() as session:
        session.execute('DELETE FROM Arquivo')
        session.commit()

# # Atualizar
# def atualizar_usuario(user):
#     with db.Session() as session:
#         existente = get_usuario(username=user.username)
        
#         if existente is None:
#             raise Exception("Usuário não existe")
        
#         existente.username = user.username
#         existente.password = user.password
#         session.commit()