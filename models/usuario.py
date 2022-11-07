from ChomikBox import *
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    Chomik = None
    logado = False
    __lista_pastas = None

    def __repr__(self):
        if self.id is not None:
            return str(self.id) + self.username
        return self.username

    def __init__(self, username='', password=''):
        if username != '' and password != '':
            self.username = username
            self.password = password
            self.Chomik = Chomik(username, password)
        else:
            self.username = ''
            self.password = ''
            self.Chomik = None
        self.logado = False

    def esta_logado(self):
        return self.logado
    
    def login(self):
        if self.Chomik is not None:
            self.Chomik.login()
            self.logado = True
            return self.logado
        self.logado = False
        return self.logado
    
    # Retorna a lista com todas as pastas da conta logada
    def listar_pastas(self):
        if self.logado:
            self.__lista_pastas = []
            root = self.Chomik.folders_list()
            #self.caminhar(pastas, root[2])
            for pasta in root:
                self.caminhar(self.__lista_pastas, pasta)
            return self.__lista_pastas
        # Retornar lista vazia se não estiver logado
        return []
    
    # Método privado para andar na lista de diretórios do chomikuj
    def caminhar(self, lista_pastas, pasta_chomik):
        # Adicionar pasta atual a lista de pastas global
        lista_pastas.append(pasta_chomik)
        parent_id = None
        if pasta_chomik.parent_folder is not None:
            parent_id = pasta_chomik.parent_folder.folder_id
        else:
            parent_id = 0

        from repositories import pasta_repository
        from models.pasta import Pasta

        pasta_repository.add_pasta(Pasta(pasta_chomik.name, pasta_chomik.password, pasta_chomik.folder_id, parent_id, pasta_chomik.path, pasta_chomik.hidden, pasta_chomik.adult, self.id))

        # Para cada pasta dentro dela faça esse método novamente
        # Se não houver pastas somente retorne
        for pasta in pasta_chomik.folders_list():
            self.caminhar(lista_pastas, pasta)
        return

    def salvar_pastas(self):
        lista = self.listar_pastas()

        for pasta in lista:
            print(pasta.path)

    def token(self):
        if self.Chomik is not None:
            return self.Chomik.get_token()
        else:
            return None
        
