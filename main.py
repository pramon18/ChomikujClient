# Teste das funcionalidades do pyChomikBox
import os
from models.pasta import Pasta

from ChomikBox import *

class Usuario:
    def __init__(self, username='', password=''):
        if username != '' and password != '':
            self.username = username
            self.__password = password
            self.Chomik = Chomik(username, password)
        else:
            self.username = ''
            self.__password = ''
            self.Chomik = None
        self.logado = False

    def esta_logado(self):
        return self.logado

    def login(self):
        if self.Chomik != None:
            print(self.Chomik.login())
            self.logado = True
            return self.logado
        self.logado = False
        return self.logado

    # Retorna a lista com todas as pastas da conta logada
    def listar_pastas(self):
        if self.logado:
            pastas = []
            root = self.Chomik.folders_list()
            #self.caminhar(pastas, root[2])
            for pasta in root:
                self.caminhar(pastas, pasta)
            return pastas
        # Retornar lista vazia se não estiver logado
        return []

    # Método privado para andar na lista de diretórios do chomikuj
    def caminhar(self, lista_pastas, pasta_chomik):
        # Adicionar pasta atual a lista de pastas global
        lista_pastas.append(pasta_chomik)
        # Para cada pasta dentro dela faça esse método novamente
        # Se não houver pastas somente retorne
        for pasta in pasta_chomik.folders_list():
            self.caminhar(lista_pastas, pasta)
        return


def salvar_pastas_arquivo(nome_arquivo, lista_pastas):
    arquivo = open(nome_arquivo, 'a')
    for pasta in lista_pastas:
        linha = '{},{},{},{},{},{},{},{}\n'.format(pasta.chomik, pasta.folder_id, pasta.name, pasta.parent_folder, pasta.hidden, pasta.adult, pasta.gallery_view, pasta.password)
        arquivo.write(linha)
    arquivo.close()

def atualizar_pastas_arquivo(nome_arquivo):
    pass

# TODO Melhorar a escrita do arquivo salvo e dar uma olhada no folder cache do chomikbox para ver o que é.
if __name__ == '__main__':
    # user = Usuario('pabloramon044', 'Pablo_Ramon044')
    # print(user.esta_logado())
    # user.login()
    # pastas_chomik = user.listar_pastas()
    # print(pastas_chomik)
    # print(len(pastas_chomik))
    # salvar_pastas_arquivo('pastas_chomikuj', pastas_chomik)
    # print('Finalizado...')
    p = Pasta(nome="pasta1")
    q = Pasta(nome="pasta2", pasta=p)
    print(p)
    print(q)
    print(p.caminho(p.nome))
    print(q.caminho(q.nome))