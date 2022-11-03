#from ChomikBox import *
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, Sequence('usuario_id_seq'),primary_key=True)
    username = Column(String)
    __password = Column(String)
    Chomik = None
    logado = False

    def __repr__(self):
        if self.id is not None:
            return str(self.id) + self.username
        return self.username

    # def __init__(self, username='', password=''):
    #     if username != '' and password != '':
    #         self.username = username
    #         self.__password = password
    #         self.Chomik = Chomik(username, password)
    #     else:
    #         self.username = ''
    #         self.__password = ''
    #         self.Chomik = None
    #     self.logado = False

    # def esta_logado(self):
    #     return self.logado
    #
    # def login(self):
    #     if self.Chomik is not None:
    #         print(self.Chomik.login())
    #         self.logado = True
    #         return self.logado
    #     self.logado = False
    #     return self.logado
    #
    # # Retorna a lista com todas as pastas da conta logada
    # def listar_pastas(self):
    #     if self.logado:
    #         pastas = []
    #         root = self.Chomik.folders_list()
    #         #self.caminhar(pastas, root[2])
    #         for pasta in root:
    #             self.caminhar(pastas, pasta)
    #         return pastas
    #     # Retornar lista vazia se não estiver logado
    #     return []
    #
    # # Método privado para andar na lista de diretórios do chomikuj
    # def caminhar(self, lista_pastas, pasta_chomik):
    #     # Adicionar pasta atual a lista de pastas global
    #     lista_pastas.append(pasta_chomik)
    #     # Para cada pasta dentro dela faça esse método novamente
    #     # Se não houver pastas somente retorne
    #     for pasta in pasta_chomik.folders_list():
    #         self.caminhar(lista_pastas, pasta)
    #     return

