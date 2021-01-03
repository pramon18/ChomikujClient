# Teste das funcionalidades do pyChomikBox
import os
from models.pasta import Pasta
from models.usuario import Usuario


# def salvar_pastas_arquivo(nome_arquivo, lista_pastas):
#     arquivo = open(nome_arquivo, 'a')
#     for pasta in lista_pastas:
#         linha = '{},{},{},{},{},{},{},{}\n'.format(pasta.chomik, pasta.folder_id, pasta.name, pasta.parent_folder, pasta.hidden, pasta.adult, pasta.gallery_view, pasta.password)
#         arquivo.write(linha)
#     arquivo.close()


# def atualizar_pastas_arquivo(nome_arquivo):
#     pass


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
