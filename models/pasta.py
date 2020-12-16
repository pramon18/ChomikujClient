from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.orm import relationship


class BasePasta():
    # Class apenas para seguir a sintaxe necessária
    # para o AnyTree
    atributo = 0

class Pasta(BasePasta):
    # __tablename__ = 'pasta'
    # id = Column(Integer, Sequence('pasta_id_seq'), primary_key=True)
    # nome = Column(String(100))
    # pasta_id = Column(Integer, ForeignKey("pasta.pasta_id"), nullable=True)
    # pasta = relationship("Pasta", backref="pasta")
    def __init__(self, nome=None, pasta=None):
        self.nome = nome
        self.pasta = pasta


    def __repr__(self):
        return f'{"<ID: "}{"self.id"}{" Nome: "}{self.nome}{">"}'

    # TODO melhor lógica do caminho
    def caminho(self, caminho):
        if self.pasta is None:
            return "/" + caminho
        return self.pasta.caminho(self.pasta.nome + "/" + self.nome)
