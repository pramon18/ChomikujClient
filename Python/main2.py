import datetime
from pathlib import Path
import time
from dotenv import load_dotenv
import requests
import json
import os
from types import SimpleNamespace

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')

class File_Id(object):
    def __init__(self, object):
        self.id = object.id
        self.success = object.success


class File(object):
    def __init__(self, object):
        self.id = object.id
        self.name = object.name
        self.size = object.size
        self.views = object.views
        self.bandwidth_used = object.bandwidth_used
        self.bandwidth_used_paid = object.bandwidth_used_paid
        self.downloads = object.downloads
        self.date_upload = object.date_upload
        self.date_last_view = object.date_last_view
        self.mime_type = object.mime_type
        self.thumbnail_href = object.thumbnail_href
        self.hash_sha256 = object.hash_sha256
        self.delete_after_date = object.delete_after_date
        self.delete_after_downloads = object.delete_after_downloads
        self.availability = object.availability
        self.availability_message = object.availability_message
        self.abuse_type = object.abuse_type
        self.abuse_reporter_name = object.abuse_reporter_name
        self.can_edit = object.can_edit
        self.can_download = object.can_download
        self.show_ads = object.show_ads
        self.allow_video_player = object.allow_video_player
        self.download_speed_limit = object.download_speed_limit

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Teste do PixelDrain
def upload_file(file):
    """
    Upload a file to pixeldrain
    
    upload_file(file)
    """
    response = requests.post(
        "https://pixeldrain.com/api/file",
        data={"anonymous": True},
        files={"file": open(file, "rb")}
    )
    return response.json()

def upload_files(files, dir_path, folder):
    for file in files:
        r = upload_file(dir_path + '/' + file)
        print(r.content)
    pass

if __name__ == '__main__':
    r = requests.get(BASE_URL + '/user/files', auth=('', API_KEY))
    
    # Load as object based on the properties names
    response = json.loads(r.content, object_hook=lambda d: SimpleNamespace(**d))

    # Parsing the response to a list of files
    files = []
    for f in response.files:
        files.append(File(f))

    for f in files:
        print(type(f))

    # print(response.files)

    # Pasta com arquivos
    dir_path = 'C:/Users/pablo/Downloads/Animes'

    # Arquivos
    compressed_files = []

    # Adicionar arquivos em uma lista
    for file in os.listdir(dir_path):
        compressed_files.append(file)

    print(compressed_files)

    # Testar upload de arquivo e separado
    start = time.time()
    upload_files(compressed_files, dir_path, "")
    end = time.time()

    print(f"Tempo de upload com os arquivos comprimidos: {(end-start)} seconds {(end-start)/60} minutes")

    pass