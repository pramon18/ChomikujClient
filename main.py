# Teste das funcionalidades do pyChomikBox
from pathlib import Path
from models.usuario import Usuario
from repositories import usuario_repository
import os
from ChomikBox import ChomikDownloader, ChomikUploader
from ChomikBox.utils.FileTransferProgressBar import FileTransferProgressBar
from utils import db
from dotenv import load_dotenv
import time
from repositories import pasta_repository
from repositories import arquivo_repository

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

class ProgressCallback(object):
    def __init__(self):
        self.bar = None
        self.stop = True

    def progress_callback(self, par):
        if isinstance(par, ChomikUploader):
            size = par.upload_size
            done = par.bytes_uploaded
        elif isinstance(par, ChomikDownloader):
            size = par.download_size
            done = par.bytes_downloaded

        if self.bar is None:
            self.bar = FileTransferProgressBar(size, par.name)
        self.bar.show(done)

        if done > size / 2 and self.stop:
            print(done)
            self.stop = False
            par.pause()

    def finish_callback(self, par):
        if isinstance(par, ChomikUploader):
            print(par.bytes_uploaded)
        elif isinstance(par, ChomikDownloader):
            print(par.bytes_downloaded)
        self.bar.done()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def downloaded(file):
    print("{}KB {} MB".format((file.bytes_downloaded / 1024), (file.bytes_downloaded / 1048576)))

def upload_file(file, filename, folder):
    callback = ProgressCallback()
    print(file.name)
    uploader = folder.upload_file(file, filename, callback.progress_callback)
    uploader.start()
    if uploader.paused:
        time.sleep(1)
        uploader.resume()
    callback.finish_callback(uploader)
    pass

def upload_files(files, dir_path, folder):
    for file in files:
        with open(dir_path + '/' + file, 'rb') as open_file:
            print(open_file.name, file)
            try:
                time.sleep(10)
                upload_file(open_file, file, folder)
            except:
                time.sleep(10)
                upload_file(open_file, file, folder)
    pass

# TODO Melhorar a escrita do arquivo salvo e dar uma olhada no folder cache do chomikbox para ver o que é.
if __name__ == '__main__':
    # Pasta com arquivos
    #dir_path = 'E:\ChomikBox'
    #dir_path = r'Files'

    # Arquivo inteiro
    #full_file = r'Files/codex-the.sims.4.get.famous(2).zip'

    # Arquivos compactados e divididos
    #compressed_files = []

    # Adicionar arquivos compactados em uma lista
    #for file in os.listdir(dir_path):
    #    compressed_files.append(file)
        #if file != 'codex-the.sims.4.get.famous(2).zip':
            #print(dir_path + '/' + file)
            #compressed_files.append(file)
    
    db.iniciar_db()
    user = None
    user = Usuario(username=os.getenv('USUARIO'), password=os.getenv('SENHA'))
    user = usuario_repository.add_usuario(user)
    print(user)
    try:
        user.login()
    except:
        raise Exception("Deu ruim")

    # A partir desse ponto tenho o usuário do Chomikuj (Hopefully)
    if(user.esta_logado()):
        user.Chomik.ssl = False
        # Listar pastas do usuário
        # print(user.Chomik.folders_list())   
        # print(user.Chomik)
        print(user.token())
        #user.listar_pastas()
        #print(pasta_repository.get_pastas_raiz())
        
        # Teste
        pasta = user.Chomik.folders_list()[4]
        print(user.Chomik.folders_list()[4])
        #user.salvar_arquivos(pasta)

        print(arquivo_repository.get_all_arquivos())

        # Testar upload de arquivo e separado
        #start = time.time()
        #upload_files(compressed_files, dir_path, pasta)
        #end = time.time()

        #print(f"Tempo de upload com os arquivos comprimidos: {(end-start)} seconds {(end-start)/60} minutes")
        

        '''
        start = time.time()
        upload_file(open(full_file, 'rb'), full_file, pasta)
        end = time.time()

        print(f"Tempo de upload com o arquivo completo: {(end-start)} seconds {(end-start)/60} minutes")
        '''

    # Download
'''
with open(listOfFiles[0].name, 'wb') as f:
    downloader = listOfFiles[0].download(f, downloaded)
    downloader.start()
    if downloader.paused:
        downloader.resume()

'''

# Upload
'''
callback = ProgressCallback()
uploader = folder.upload_file(open('Ijiranaide Nagatoro-san.zip', 'rb'), 'Ijiranaide Nagatoro-san(1).zip', callback.progress_callback)
uploader.start()
if uploader.paused:
    time.sleep(1)
    uploader.resume()
callback.finish_callback(uploader)
'''

# TODO Salvar arquivos a serem baixados no banco de dados
# TODO Ver que informações da biblioteca são necessárias para o modelo
# TODO Sincronizar informações salvas no banco e no Chomikuj
