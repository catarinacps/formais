class Nodo():
    def __init__(self, producao=None):
        self.producao = producao
        self.filhos = [None for x in producao]

    def gera_filho(self, variavel, producao):
        for index, item  in enumerate(self.producao):
            if variavel == item and self.filhos[index] != None:
                self.filhos[index] = producao
                break
            
    #Diz se o nodo atual está completo em produções possiveis na sua árvore
    def todos_filhos(self):
        for index, item in enumerate(self.filhos):
            if item == None and self.producao[index].isupper():
                return False

        return True   
   def primeiro_livre(self ):
        if self.todos_filhos():


class Arvore():
    def __init__(self):
        self.raiz = Nodo()

    def adiciona_nodo(self, variavel, producao):
        if self.raiz.todos_filhos():
            
        else:
            self.raiz.gera_filho(variavel,producao)

 