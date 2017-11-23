VAZIO = u'\u03B5'

class Derivacao:
    def __init__(self, elementos):
        self.derivados = []
        self.derivados.append(elementos)

    def __str__(self):
        return ' | '.join(self.__rep_regras())

    def __repr__(self):
        return ' | '.join(self.__rep_regras())

    def acrescenta_derivacao(self, elementos):
        self.derivados.append(elementos)

    def remove_derivacao(self, elementos):
        self.derivados = [val for val in self.derivados if val != elementos]

    def gera_vazio(self):
        if [VAZIO] in self.derivados:
            return True
        return False

    def gera_chave(self, key):
        for derivacao in self.derivados:
            if key in derivacao:
                return derivacao
        return False

    def remove_ocorrencias_variavel(self, variavel):
        for indice, derivacao in enumerate(self.derivados):
            self.derivados[indice] = [val for val in derivacao if val != variavel]

    def duplica_derivacoes(self, variavel):
        for derivacao in self.derivados:
            if variavel in derivacao:
                novas_derivacoes = [val for val in derivacao if val != variavel]
                if novas_derivacoes:
                    self.acrescenta_derivacao(novas_derivacoes)
                else:
                    self.acrescenta_derivacao([VAZIO])


    def __rep_regras(self):
        lista_strings = []
        for deriv in self.derivados:
            lista_strings.append(' '.join(deriv))
        return lista_strings
