class ChomikFolder(object):
    def __init__(self, chomik, name, folder_id, parent_folder, hidden, adult, gallery_view, password):
        #assert isinstance(chomik, Chomik)
        #assert isinstance(name, ustr)
        #assert isinstance(parent_folder, ChomikFolder) or parent_folder is None
        #assert isinstance(hidden, bool)
        #assert isinstance(adult, bool)
        #assert isinstance(gallery_view, bool)

        self.chomik, self.folder_id, self.name = chomik, int(folder_id), name
        self.parent_folder, self.hidden, self.adult, self.gallery_view = parent_folder, hidden, adult, gallery_view
        self.password = password

    def __repr__(self):
        return '<ChomikBox.ChomikFolder: "{p}" ({c})>'.format(p=self.path, c=self.chomik.name)

    @property
    def path(self):
        return self.parent_folder.path + self.name + '/'

    '''
    @classmethod
    def cache(cls, chomik, name, folder_id, parent_folder, hidden, adult, gallery_view, password):
        assert isinstance(chomik, Chomik)
        folder_id = int(folder_id)
        if folder_id in chomik._folder_cache:
            assert isinstance(name, ustr)
            assert isinstance(parent_folder, ChomikFolder)
            assert isinstance(hidden, bool)
            assert isinstance(adult, bool)
            assert isinstance(gallery_view, bool)
            fol = chomik._folder_cache[folder_id]
            fol.name, fol.parent_folder, fol.hidden, fol.adult, fol.gallery_view = name, parent_folder, hidden, adult, gallery_view
            fol.password = password
        else:
            fol = cls(chomik, name, folder_id, parent_folder, hidden, adult, gallery_view, password)
            chomik._folder_cache[folder_id] = fol
        return fol
    
    def __iter__(self):
        return iter(self.list())

    def files_list(self, only_downloadable=False):
        return self.chomik.files_list(only_downloadable, self)

    def folders_list(self):
        return self.chomik.folders_list(self)

    def list(self, only_downloadable=False):
        return self.folders_list() + self.files_list(only_downloadable)

    def get_folder(self, name, case_sensitive=True):
        assert isinstance(name, ustr)
        if case_sensitive:
            for f in self.folders_list():
                if f.name == name:
                    return f
        else:
            name = str_casefold(name)
            for f in self.folders_list():
                if str_casefold(f.name) == name:
                    return f

    def get_file(self, name, case_sensitive=True):
        assert isinstance(name, ustr)
        if case_sensitive:
            for f in self.files_list():
                if f.name == name:
                    return f
        else:
            name = str_casefold(name)
            for f in self.files_list():
                if str_casefold(f.name) == name:
                    return f

    def get(self, name, case_sensitive=True):
        assert isinstance(name, ustr)
        found = self.get_folder(name, case_sensitive)
        if found is None:
            found = self.get_file(name, case_sensitive)
        return found
    '''    
    