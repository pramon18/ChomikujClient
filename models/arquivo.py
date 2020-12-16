
class BaseArquivo():
    # Class apenas para seguir a sintaxe necessária
    # para o AnyTree
    atributo = 0


class Arquivo(BaseArquivo):
    def __init__(self, nome=None, pasta=None):
        self.nome = nome
        self.pasta = pasta

        if not nome:
            raise NameError("Nome não pode ser vazio")