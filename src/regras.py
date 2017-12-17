from src.tree import *

VAZIO = u'\u03B5'
BULLET = u'\u2022'


class Derivacao:
    def __init__(self, elementos=None):
        self.derivados = []
        self.variaveis_geradas = []
        self.terminais_gerados = []
        if elementos:
            self.derivados.append(elementos)
            for simbolo in elementos:
                if simbolo not in self.variaveis_geradas and (simbolo.isupper() and simbolo != VAZIO):
                    self.variaveis_geradas.append(simbolo)
                if simbolo not in self.terminais_gerados and (simbolo.islower() or simbolo == VAZIO):
                    self.terminais_gerados.append(simbolo)

    def __str__(self):
        return ' | '.join(self.__rep_regras())

    def __repr__(self):
        return ' | '.join(self.__rep_regras())

    def acrescenta_derivacao(self, elementos):
        self.derivados.append(elementos)
        for simbolo in elementos:
            if simbolo not in self.variaveis_geradas and (simbolo.isupper() and simbolo != VAZIO):
                self.variaveis_geradas.append(simbolo)
            if simbolo not in self.terminais_gerados and (simbolo.islower() or simbolo == VAZIO):
                self.terminais_gerados.append(simbolo)

    def remove_derivacao(self, regra):
        self.derivados = [val for val in self.derivados if val != regra]
        self.variaveis_geradas = []
        for deriv in self.derivados:
            for simbolo in deriv:
                if simbolo not in self.variaveis_geradas and (simbolo.isupper() and simbolo != VAZIO):
                    self.variaveis_geradas.append(simbolo)
                if simbolo not in self.terminais_gerados and (simbolo.islower() or simbolo == VAZIO):
                    self.terminais_gerados.append(simbolo)

    def remove_derivacao_considerando_variavel(self, variavel):
        copia_derivados = self.derivados.copy()
        self.variaveis_geradas.remove(variavel)
        for derivacao in copia_derivados:
            if variavel in derivacao:
                self.remove_derivacao(derivacao)

    def gera_vazio(self):
        if VAZIO in self.terminais_gerados:
            return True
        return False

    def gera_variavel(self, key=None):
        if key:
            if key in self.variaveis_geradas:
                return True
            else:
                return False
        elif self.variaveis_geradas:
            return True
        return False

    def gera_terminal(self, key=None):
        if key:
            if key in self.terminais_gerados:
                return True
            else:
                return False
        elif self.terminais_gerados:
            return True
        return False

    def remove_ocorrencias_variavel(self, variavel):
        for indice, derivacao in enumerate(self.derivados):
            self.derivados[indice] = [val for val in derivacao if val != variavel]
        self.derivados = [x for x in self.derivados if x != []]

    def duplica_derivacoes(self, variavel):
        copia_derivados = self.derivados.copy()
        for item_derivacao in copia_derivados:
            novas_derivacoes = [[]]
            for indice_simbolo, simbolo in enumerate(item_derivacao):
                copia_novas_derivacoes = novas_derivacoes.copy()
                for indice_novo, novo in enumerate(copia_novas_derivacoes):
                    derivacao_atual = novo.copy()
                    novas_derivacoes[indice_novo].append(simbolo)
                    if simbolo == variavel:
                        novas_derivacoes.append(derivacao_atual)
            for derivacao_acrescentavel in novas_derivacoes:
                if derivacao_acrescentavel not in self.derivados and derivacao_acrescentavel:
                    self.derivados.append(derivacao_acrescentavel)

    def __rep_regras(self):
        lista_strings = []
        for deriv in self.derivados:
            lista_strings.append(' '.join(deriv))
        return lista_strings


class DerivacaoEarley(Derivacao):
    def __init__(self, elementos=None, arvore=None, variavel=None):
        self.derivados = []
        self.variaveis_geradas = []
        self.terminais_gerados = []
        self.lista_arvores = []
        if elementos:
            if arvore and variavel:
                self.lista_arvores.append(arvore.adiciona_nodo(variavel, elementos))
            else:
                self.lista_arvores.append(Arvore(elementos))
            self.derivados.append(elementos)
            for simbolo in elementos:
                if simbolo not in self.variaveis_geradas and (simbolo.isupper() and simbolo != VAZIO):
                    self.variaveis_geradas.append(simbolo)
                if simbolo not in self.terminais_gerados and (simbolo.islower() or simbolo == VAZIO):
                    self.terminais_gerados.append(simbolo)

    def acrescenta_derivacao(self, elementos, arvore=None, variavel=None):
        if elementos not in self.derivados:
            if arvore and variavel:
                self.lista_arvores.append(arvore.adiciona_nodo(variavel, elementos))
            else:
                self.lista_arvores.append(Arvore(elementos))
            self.derivados.append(elementos)
            for simbolo in elementos:
                if simbolo not in self.variaveis_geradas and (simbolo.isupper() and simbolo != VAZIO):
                    self.variaveis_geradas.append(simbolo)
                if simbolo not in self.terminais_gerados and (simbolo.islower() or simbolo == VAZIO):
                    self.terminais_gerados.append(simbolo)

    def __rep_regras(self):
        lista_strings = []
        for deriv in self.derivados:
            lista_strings.append(' '.join(deriv))
        return lista_strings

    def lista_producoes(self):
        return self.__rep_regras()
