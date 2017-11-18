class Regra:
    def __init__(self, elementos):
        self.variavel = elementos[0]
        self.derivados = elementos[1:]

    def __str__(self):
        return self.variavel + ' -> ' + ' '.join(self.derivados)
    
    def __repr__(self):
        return self.variavel + ' -> ' + ' '.join(self.derivados)
