import re

class Gramatica:
    def __init__(self, abspath):
        with open(abspath, 'r') as textFile:
            regexTerminais = re.compile('[a-z]((?<=^\[ )(?= \])(?<!.*#.*))')
            regexRegras = re.compile('\w((?<=\[ )(?= \])(?<!.*#.*))')
            regexVariaveis = re.compile('[A-Z]((?<=^\[ )(?= \])(?<!.*#.*)(?! \] >))')

            self.terminais = []
            self.variaveis = []
            self.inicial = ''
            self.regras = []

            secao = 0
            for linha in textFile:
                if __decodeSection__(self, linha) == 1:
                    secao += 1
                    continue
                
                if secao == 1:
                    terminaisEncontrados = regexTerminais.findall(linha)
                    for match in terminaisEncontrados:
                        if match != '':
                            self.terminais.append(match)
                elif secao == 2:
                    variaveisEncontradas = regexVariaveis.findall(linha)
                    for match in variaveisEncontradas:
                        if match != '':
                            self.variaveis.append(match)
                elif secao == 3:
                    inicialEncontrado = regexVariaveis.findall(linha)
                    for match in inicialEncontrado:
                        if match != '':
                            self.inicial = match
                elif secao == 4:
                    regrasEncontradas = regexRegras.findall(linha)
                    for match in regrasEncontradas:
                        if match != '':
                            self.regras.append(match)
                else:
                    print('not suposed to happen, sry')
                    return

    def __decodeSection__(self, line):
        regexSecao = re.compile('^(#Terminais|#Variaveis|#Inicial|#Regras)')

        header = regexSecao.search(line)

        if header.group() != '':
            return 1
        else:
            return 0

    def __str__(self):
        return 'Terminais: ' + str(self.terminais) + '\nVariaveis: ' + str(self.variaveis) + '\nInicial: ' + self.inicial + '\nRegras: ' + str(self.regras)
