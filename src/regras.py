class Derivacao:
    def __init__(self, elementos):
        self.derivados = []
        self.derivados.append(elementos)

    def __str__(self):
        return ' -> ' + ' | '.join(self.__rep_regras())

    def __repr__(self):
        return ' -> ' + ' | '.join(self.__rep_regras())

    def append_derivacao(self, elementos):
        self.derivados.append(elementos)

    def gera_vazio(self):
        if ['V'] in self.derivados:
            return True
        else:
            return False

    def gera_chave(self, key):
        if [key] in self.derivados:
            return True
        else:
            return False

    def __rep_regras(self):
        lista_strings = []
        for deriv in self.derivados:
            lista_strings.append(' '.join(deriv))
        return lista_strings
