# Teste das funcionalidades do pyChomikBox
from models.usuario import Usuario
from repositories import usuario_repository
import os
from ChomikBox import ChomikDownloader, ChomikUploader
from ChomikBox.utils.FileTransferProgressBar import FileTransferProgressBar
from utils import db

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

# TODO Melhorar a escrita do arquivo salvo e dar uma olhada no folder cache do chomikbox para ver o que é.
if __name__ == '__main__':
    db.iniciar_db()
    user = None
    user = Usuario(username="usuario", password="senha_secreta")
    user = usuario_repository.add_usuario(user)

    try:
        user.login()
    except:
        raise Exception("Deu ruim")

    # A partir desse ponto tenho o usuário do Chomikuj (Hopefully)
    if(user.esta_logado()):
        # Listar pastas do usuário
        print(user.Chomik.folders_list())   

        # Teste
        print(user.listar_pastas())
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
