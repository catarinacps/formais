import re
from src.regras import *

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
            regex_terminais = re.compile(r'(?<=^\[ )[a-z](?= \])', re.A)
            regex_regras = re.compile(r'(?<=\[ )\w(?= \])', re.A)
            regex_variaveis = re.compile(r'(?<=^\[ )[A-Z](?= \])', re.A)
            regex_secao = re.compile(r'^(#Terminais|#Variaveis|#Inicial|#Regras)', re.A)

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
                if regex_secao.search(linha) != None:
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
                    terminaisEncontrados = regex_terminais.findall(linha)
                    for match in terminaisEncontrados:
                        if match != '':
                            self.terminais.append(match)
                elif secao == 2:
                    # Seção == 2 -> #Variaveis
                    # Procuro as Variaveis que aparecem na linha, e, se existirem, coloco na lista
                    variaveisEncontradas = regex_variaveis.findall(linha)
                    for match in variaveisEncontradas:
                        if match != '':
                            self.variaveis.append(match)
                elif secao == 3:
                    # Seção == 3 -> #Inicial
                    # Procuro o Inicial que aparece na linha, e, se existir, guardo
                    inicialEncontrado = regex_variaveis.findall(linha)
                    for match in inicialEncontrado:
                        if match != '':
                            self.inicial = match
                elif secao == 4:
                    # Seção == 4 -> #Regras
                    # Procuro as Regras que aparecem na linha, e, se existirem, coloco na lista
                    regrasEncontradas = regex_regras.findall(linha)
                    listaRegras = []
                    for match in regrasEncontradas:
                        if match != '':
                            if match != 'V':
                                listaRegras.append(match)
                            else:
                                listaRegras.append(VAZIO)

                    variavel = listaRegras[0]
                    if variavel not in self.regras:
                        self.regras[variavel] = Derivacao(listaRegras[1:])
                    else:
                        self.regras[variavel].acrescenta_derivacao(listaRegras[1:])
                else:
                    # Default do meu pseudo-switch
                    print('not supposed to happen, sry')
                    return

    def __str__(self):
        return ('Terminais: ' + ', '.join(self.terminais) + '\nVariaveis: ' + ', '.join(self.variaveis) +
                '\nInicial: ' + self.inicial + '\nRegras: \n' + self.__rep_dict())

    def simplificar(self):
        fecho_vazio = []
        for chave, valor in self.regras.items():
            if valor.gera_vazio():
                fecho_vazio.append(chave)
        for variavel in fecho_vazio:
            fecho_vazio += list(set(self.__fecho_indireto(variavel)) - set(fecho_vazio))

        copia_auxiliar = self.regras.copy()
        for variavel, derivacao in copia_auxiliar.items():
            if variavel != self.inicial and derivacao.gera_vazio():
                if len(derivacao.derivados) == 1:
                    self.__remove_variavel(variavel)
                else:
                    self.regras[variavel].remove_derivacao([VAZIO])
        copia_auxiliar = self.regras.copy()
        for variavel, derivacao in copia_auxiliar.items():
            for gerador_vazio in fecho_vazio:
                if derivacao.gera_chave(gerador_vazio):
                    self.regras[variavel].duplica_derivacoes(gerador_vazio)

    def __fecho_indireto(self, variavel):
        lista_geradora = []
        for chave, valor in self.regras.items():
            if variavel in valor.variaveis_geradas and variavel not in lista_geradora:
                lista_geradora.append(chave)
        return lista_geradora

    def __remove_variavel(self, variavel):
        self.regras.pop(variavel, None)
        self.variaveis.remove(variavel)
        for chave, valor in self.regras.items():
            valor.remove_ocorrencias_variavel(variavel)

    def __remove_simbolos_inuteis(self):
        copia_auxiliar_var, copia_auxiliar_reg = self.variaveis.copy(), self.regras.copy()
        for variavel in copia_auxiliar_var:
            if variavel not in self.regras:
                self.variaveis.remove(variavel)
                for chave, valor in copia_auxiliar_reg:
                    if variavel in valor.variaveis_geradas:
                        self.regras[chave].remove_derivacao_considerando_variavel(variavel)

        fecho_atingivel_variaveis = [self.inicial]
        fecho_atingivel_terminais = []
        #LITERALMENTE MORRENDO DE FOME

    def __rep_dict(self):
        string = ''
        for key, value in self.regras.items():
            string += key + ' -> ' + str(value) + '\n'
        return string
