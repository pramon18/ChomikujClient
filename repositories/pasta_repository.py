from utils import db
from models.pasta import Pasta

## Consultas

# Buscar pasta
def get_pasta(pasta_id):
    with db.Session() as session:
        return session.query(Pasta).filter_by(pasta_id=pasta_id).first()

## Operacoes
# Adicionar
def add_pasta(pasta):
    with db.Session() as session:
        existente = get_pasta(pasta_id=pasta.pasta_id)
        
        if existente is not None:
            return existente

        session.add(pasta)
        session.commit()
        return get_pasta(pasta_id=pasta.pasta_id)

# # Deletar
# def delete_usuario(user):
#     with db.Session() as session:
#         existente = get_usuario(username=user.username)
        
#         if existente is None:
#             raise Exception("Usuário não existe")
        
#         session.delete(user)
#         session.commit()

# # Atualizar
# def atualizar_usuario(user):
#     with db.Session() as session:
#         existente = get_usuario(username=user.username)
        
#         if existente is None:
#             raise Exception("Usuário não existe")
        
#         existente.username = user.username
#         existente.password = user.password
#         session.commit()