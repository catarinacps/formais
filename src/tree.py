class Nodo():
    def __init__(self, producao):
        self.producao = producao
        self.filhos = [None for x in producao]
        self.proximo = 0             # Variavel que determina qual o próximo da árvore a ser modificado

    def gera_filho(self, variavel, producao):
        if not self.todos_filhos():
            if variavel == self.producao[self.proximo] and self.filhos[self.proximo] is None:
                nodo_filho = Nodo(producao)
                self.filhos[self.proximo] = nodo_filho
                self.proximo += 1

                while not self.todos_filhos() and self.producao[self.proximo].islower():
                    self.proximo += 1
                return True
        return False

    # Diz se o nodo atual está completo em produções possiveis na sua árvore
    def todos_filhos(self):
        for index, item in enumerate(self.filhos):
            if item is None and self.producao[index].isupper():
                return False
        return True


class Arvore():
    def __init__(self, var_base):
        self.raiz = Nodo(var_base)

    def adiciona_nodo(self, variavel, producao):
        return self.__ad_nodo(self.raiz, variavel, producao)

    def __ad_nodo(self, nodo, variavel, producao):
        if nodo.gera_filho(variavel, producao):
            return True
        else:
            for filho in nodo.filhos:
                if filho != None and self.__ad_nodo(filho, variavel, producao):
                    return True

    # Dado um terminal, move o próximo para o símbolo seguinte quando o próximo está apontando para esse terminal
    def move_proximo(self, terminal):
        return False
