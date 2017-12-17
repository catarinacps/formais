class Nodo():
    def __init__(self, producao=None):
        self.producao = producao
        self.filhos = [None for x in producao]

    def gera_filho(self, variavel, producao):
        for items in self.producao:
            if variavel in self.producao:
                if self.filhos[self.producao.index(variavel)] != None:
                    self.filhos[self.producao.index(variavel)] = Nodo(producao)


class Arvore():
    def __init__(self):
        self.raiz = Nodo()

    def adiciona_nodo(self, )
