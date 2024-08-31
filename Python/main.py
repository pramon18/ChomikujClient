# Teste das funcionalidades do pyChomikBox
import sys
from models.usuario import Usuario
import os
from ChomikBox import ChomikDownloader, ChomikUploader
from ChomikBox.utils.FileTransferProgressBar import FileTransferProgressBar
import time

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
        with open(dir_path + '/' + file, '+rb') as open_file:
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
    # Definir parâmetros
    # Caminho a verificar?
    
    # Pegar parâmetros
    if len(sys.argv) > 1:
        print(sys.argv)
        
        input_path = None
        chomik_output_path = None
        
        # Recuperar diretório de busca
        try:
            input_path = sys.argv[1]
        except:
            pass
        
        # Recuperar diretório de destino
        try:
            chomik_output_path = sys.argv[2]
        except:
            pass
        
        # Lista de arquivos a serem enviados
        dir_files = []
               
        # Listar arquivos e pastas no caminho buscado
        for file in os.listdir(input_path):
            print(file)
            dir_files.append(file)
            
        # Tentar logar no chomikuj
        user = None
        user = Usuario(username=os.getenv('USUARIO'), password=os.getenv('SENHA'))

        try:
            user.login()
        except:
            raise Exception("Erro ao fazer login.")
        
        # Ajustar SSL
        if(user.esta_logado()):
            user.Chomik.ssl = False
        
        # Buscar pasta de destino
        for file in user.Chomik.folders_list():
            print(file.path)
            
        destination_folder = list(filter(lambda x: chomik_output_path in x.path, user.Chomik.folders_list()))[0]
        
        # Enviar
        print(dir_files)
        print(destination_folder)
        
        # try:
        #     upload_files(dir_files, input_path, destination_folder)
        # except:
        #     print("Erro ao enviar arquivos.")
        #     pass
        
        for file in dir_files:
            callback = ProgressCallback()
            uploader = destination_folder.upload_file(open(input_path + '/' + file, '+rb'), file, callback.progress_callback)
            uploader.start()
            if uploader.paused:
                time.sleep(1)
                uploader.resume()
            callback.finish_callback(uploader)

# TODO Salvar arquivos a serem baixados no banco de dados
# TODO Ver que informações da biblioteca são necessárias para o modelo
# TODO Sincronizar informações salvas no banco e no Chomikuj
