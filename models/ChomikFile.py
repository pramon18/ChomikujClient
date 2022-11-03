class ChomikFile(object):
    def __init__(self, chomik, name, file_id, parent_folder, size, url=None):
        #assert isinstance(chomik, Chomik)
        #assert isinstance(name, ustr)
        #assert isinstance(parent_folder, ChomikFolder)
        #assert isinstance(url, ustr) or url is None

        self.chomik, 
        self.name, 
        self.file_id = chomik, 
        name, 
        int(file_id)
        self.parent_folder, 
        self.size, 
        self.url = parent_folder, 
        size, 
        url

    def __repr__(self):
        return '<ChomikBox.ChomikFile: "{p}"{i}({c})>'.format(p=self.path, i=' ' if self.downloadable else '-not downloadable- ', c=self.chomik.name)

    '''
    def open(self):
        if self.downloadable:
            return SeekableHTTPFile(self.url, self.name, self.chomik.sess)
    '''

    @property
    def downloadable(self):
        return self.url is not None

    @property
    def path(self):
        return self.parent_folder.path + self.name

    '''
    def rename(self, name, description):
        return self.chomik.rename_file(name, description, self)

    def move(self, to_folder):
        return self.chomik.move_file(self, to_folder)

    def remove(self):
        return self.chomik.remove_file(self)

    def download(self, file_like, progress_callback=None):
        return ChomikDownloader(self.chomik, self, file_like, progress_callback)
    '''