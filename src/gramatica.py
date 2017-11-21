import re
from src.regras import Derivacao

class Gramatica:
    """Classe Gramatica, que representa uma gramatica qualquer.

    Dependencias:
        re
    """
    def __init__(self, abspath):
        """Construtor da classe Gramatica, que busca padroes regex e inicializa os seus atributos.

        Entrada:
        abspath -   uma string com o caminho para o arquivo de texto
        """

        # A abertura do bloco a seguir é a maneira correta de usar arquivos em python.
        # Dessa maneira, o HANDLE do arquivo vai pra variável "textFile" e ele é fechado
        # automaticamente ao chegar no fim do bloco.
        with open(abspath, 'r') as textFile:
            # A segur estão as regras de regex que eu criei pra pegar as coisas de arquivos de texto
            regexTerminais = re.compile(r'(?<=^\[ )[a-z](?= \])', re.A)
            regexRegras = re.compile(r'(?<=\[ )\w(?= \])', re.A)
            regexVariaveis = re.compile(r'(?<=^\[ )[A-Z](?= \])', re.A)
            regexSecao = re.compile(r'^(#Terminais|#Variaveis|#Inicial|#Regras)', re.A)

            # Aqui eu inicializo os atributos do futuro objeto de Gramática, onde:
            self.terminais = []
            # é uma lista de strings contendo os terminais
            self.variaveis = []
            # é uma lista de strings contendo as variáveis
            self.inicial = ''
            # é a string que guarda a variável inicial
            self.regras = {}
            # é um dicionario de objetos Derivacao.
            # Cada chave e seu respectivo valor representam
            # {'S': ['S', 'a'], ...}   <->     S -> S a, ...

            # A variável "secao" representa uma flag de controle pra um pseudo-switch futuro
            secao = 0
            # Esse loop for vai iterar sobre cada linha do arquivo em "textFile". Isso é uma das
            # magias de python. Como ele sabe como iterar sobre cada linha do arquivo nessa sintaxe
            # simples e limpa? Não faço ideia.
            for linha in textFile:
                # A função na próxima linha aplica uma regra de expressões regulares na linha,
                # procurando as palavras-chave de seção, que indicam o início de uma nova seção
                if regexSecao.search(linha) != None:
                    # Se a função algo diferente de None, é hora de trocar de seção
                    secao += 1
                    # o que é representado por eu incrementar a variável ali em cima
                    # e passar pra próxima linha
                    continue

                linha = linha.split('#')[0]
                # Eis um pseudo-switch. Python é uma das poucas linguagens que não tem switch.
                # Sei lá por que não tem. Ninguém realmente sabe porque na verdade.
                if secao == 1:
                    # Seção == 1 -> #Terminais
                    # Procuro os terminais que aparecem na linha, e, se existirem, coloco na lista
                    terminaisEncontrados = regexTerminais.findall(linha)
                    for match in terminaisEncontrados:
                        if match != '':
                            self.terminais.append(match)
                elif secao == 2:
                    # Seção == 2 -> #Variaveis
                    # Procuro as Variaveis que aparecem na linha, e, se existirem, coloco na lista
                    variaveisEncontradas = regexVariaveis.findall(linha)
                    for match in variaveisEncontradas:
                        if match != '':
                            self.variaveis.append(match)
                elif secao == 3:
                    # Seção == 3 -> #Inicial
                    # Procuro o Inicial que aparece na linha, e, se existir, guardo
                    inicialEncontrado = regexVariaveis.findall(linha)
                    for match in inicialEncontrado:
                        if match != '':
                            self.inicial = match
                elif secao == 4:
                    # Seção == 4 -> #Regras
                    # Procuro as Regras que aparecem na linha, e, se existirem, coloco na lista
                    regrasEncontradas = regexRegras.findall(linha)
                    listaRegras = []
                    for match in regrasEncontradas:
                        if match != '':
                            listaRegras.append(match)

                    variavel = listaRegras[0]
                    if variavel not in self.regras:
                        self.regras[variavel] = Derivacao(listaRegras[1:])
                    else:
                        self.regras[variavel].append_derivacao(listaRegras[1:])
                else:
                    # Default do meu pseudo-switch
                    print('not supposed to happen, sry')
                    return

    def __str__(self):
        return ('Terminais: ' + ', '.join(self.terminais) + '\nVariaveis: ' + ', '.join(self.variaveis) +
                '\nInicial: ' + self.inicial + '\nRegras: \n' + self.__rep_dict())

    def __rep_dict(self):
        string = ''
        for key, value in self.regras.items():
            string += key + str(value) + '\n'
        return string
