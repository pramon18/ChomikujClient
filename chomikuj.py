import os
import time
from ChomikBox import Chomik, ChomikDownloader, ChomikUploader
from ChomikBox.utils.FileTransferProgressBar import FileTransferProgressBar

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

c = Chomik('pabloramon044', 'Runes.Alfeus044')
c.login()
print(c)
c.ssl = False
l = c.list()

## Arquivo que serão apagados
#print(l[0])
#print(l[0].files_list())

print(l[1])

listOfFiles = l[1].files_list()
folder = l[1]

for file in listOfFiles:
    print(file)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def downloaded(file):
    print("{}KB {} MB".format((file.bytes_downloaded / 1024), (file.bytes_downloaded / 1048576)))

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
