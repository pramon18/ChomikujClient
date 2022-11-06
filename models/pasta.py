from sqlalchemy import Column, Integer, Sequence, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

'''
class BasePasta():
    # Class apenas para seguir a sintaxe necessária
    # para o AnyTree
    atributo = 0
'''

class Pasta(Base):
    __tablename__ = 'pasta'
    id = Column(Integer, Sequence('pasta_id_seq'), primary_key=True)
    nome = Column(String(100))
    pasta_id = Column(Integer, ForeignKey("pasta.pasta_id"), nullable=True)
    parent_id = Column(Integer, nullable=True)
    hidden = Column(Boolean)
    adult = Column(Boolean)
    password = Column(String, nullable=True)
    path = Column(String, nullable=True)
    usuario_id = Column(String, nullable=True)

    def __init__(self, nome=None, password=None, pasta_id=None, parent_id=None, path=None, hidden=False, adult=False, usuario_id=None):
        self.nome = nome
        self.password = password
        self.pasta_id = pasta_id
        self.parent_id = parent_id
        self.path = path
        self.hidden = hidden
        self.adult = adult
        self.usuario_id = usuario_id

    def __repr__(self):
        return f'{"<ID: "}{"self.id"}{" Nome: "}{self.nome}{">"}'

    # TODO melhor lógica do caminho
    def caminho(self, caminho):
        if self.pasta is None:
            return "/" + caminho
        return self.pasta.caminho(self.pasta.nome + "/" + self.nome)
