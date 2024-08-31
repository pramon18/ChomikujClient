from utils import db
from models.pasta import Pasta

## Consultas

# Buscar pasta
def get_pasta(pasta_id):
    with db.Session() as session:
        return session.query(Pasta).filter_by(pasta_id=pasta_id).first()

# Buscar pastas raiz
def get_pastas_raiz():
    with db.Session() as session:
        return session.query(Pasta).filter_by(parent_id=0).all()

# Buscar pastas vazias
def get_pastas_vazias():
    with db.Session() as session:
        sql = 'select pasta.id, pasta.nome, pasta.pasta_id, pasta.parent_id, pasta.hidden, pasta.adult, pasta.password, pasta.path, pasta.usuario_id from pasta left join arquivo on arquivo.parent_id = pasta.pasta_id where arquivo.id is null;'
        result = session.query(Pasta).from_statement(db.text(sql)).all()
        return result

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

def delete_all_pastas():
    with db.Session() as session:
        session.execute('DELETE FROM Pasta')
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