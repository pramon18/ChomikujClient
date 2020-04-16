# Teste das funcionalidades do pyChomikBox

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

user = Usuario('pabloramon044', 'Pablo_Ramon044')
print(user.esta_logado())
user.login()