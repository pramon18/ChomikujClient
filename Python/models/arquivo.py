from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

'''
class BaseArquivo():
    # Class apenas para seguir a sintaxe necessária
    # para o AnyTree
    atributo = 0
'''

class Arquivo(Base):
    __tablename__ = 'arquivo'
    id = Column(Integer, Sequence('arquivo_id_seq'), primary_key=True)
    nome = Column(String(100))
    arquivo_id = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
    path = Column(String, nullable=True)
    usuario_id = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    url = Column(String, nullable=True)

    def __init__(self, nome=None, arquivo_id=None, parent_id=None, path=None, usuario_id=None, size=None, url=None):
        self.nome = nome
        self.arquivo_id = arquivo_id
        self.parent_id = parent_id
        self.path = path
        self.usuario_id = usuario_id
        self.size = size
        self.url = url

    def __repr__(self):
        return f'{"<ID: "}{self.id}{" Nome: "}{self.nome}{">"}'

    def caminho(self, caminho):
        if self.pasta is None:
            return "/" + caminho
        return self.pasta.caminho(self.pasta.nome + "/" + self.nome)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}