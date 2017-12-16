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
            regex_terminais = re.compile(r'(?<=^\[ )[a-z](?= \])')
            regex_regras = re.compile(r'(?<=\[ )\w(?= \])')
            regex_variaveis = re.compile(r'(?<=^\[ )[A-Z](?= \])')
            regex_secao = re.compile(r'^(#Terminais|#Variaveis|#Inicial|#Regras)')

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
                if derivacao.gera_variavel(key=gerador_vazio):
                    self.regras[variavel].duplica_derivacoes(gerador_vazio)

        fecho_variaveis = {}

        for variavel in self.variaveis:
            fecho_variaveis[variavel] = []
            fecho_variaveis[variavel] = self.__fecho_transitivo(fecho_variaveis, variavel, variavel)

        for variavel in self.variaveis:
            novas_producoes = Derivacao()
            for producao in self.regras[variavel].derivados:
                if len(producao) == 1 and producao[0].islower() and producao not in novas_producoes.derivados:
                    novas_producoes.acrescenta_derivacao(producao)
                elif len(producao) >= 2 and producao not in novas_producoes.derivados:
                    novas_producoes.acrescenta_derivacao(producao)
            for var in fecho_variaveis[variavel]:
                for producao in self.regras[var].derivados:
                    if len(producao) == 1 and producao[0].islower() and producao not in novas_producoes.derivados:
                        novas_producoes.acrescenta_derivacao(producao)
                    elif len(producao) >= 2 and producao not in novas_producoes.derivados:
                        novas_producoes.acrescenta_derivacao(producao)
            self.regras[variavel] = novas_producoes

        self.__remove_simbolos_inuteis()

    def chomsky(self):
        self.simplificar()

        copia_auxiliar_reg = self.regras.copy()
        for variavel, derivacao in copia_auxiliar_reg.items():
            for indice_deriv, producao in enumerate(derivacao.derivados):
                for indice_prod, simbolo in enumerate(producao):
                    if simbolo.islower():
                        nova_var = self.__gera_nome_variavel_terminal(simbolo)
                        if nova_var not in self.regras:
                            self.variaveis.append(nova_var)
                            self.regras[nova_var] = Derivacao(simbolo)
                        self.regras[variavel].derivados[indice_deriv][indice_prod] = nova_var

        copia_auxiliar_reg = list(self.regras.items())
        for variavel, derivacao in copia_auxiliar_reg:
            for indice_deriv, producao in enumerate(derivacao.derivados):
                if len(producao) > 2:
                    nova_producao = producao[1:]
                    nova_var = self.__gera_nome_variavel_agrupamento(nova_producao)
                    if nova_var not in self.regras:
                        self.variaveis.append(nova_var)
                        self.regras[nova_var] = Derivacao(nova_producao)
                        copia_auxiliar_reg.append((nova_var, Derivacao(nova_producao)))
                    self.regras[variavel].remove_derivacao(producao)
                    self.regras[variavel].acrescenta_derivacao([producao[0], nova_var])

    def earley(self, palavra):
        tamanho_palavra = len(palavra)

        tabela_passos = []

        lista_vars = []
        tabela_passos.append({self.inicial: DerivacaoEarley()})
        for producao in self.regras[self.inicial].derivados:
            tabela_passos[0][self.inicial].acrescenta_derivacao([BULLET] + producao + ['/0'])
            if producao[0].isupper():
                lista_vars += [producao[0]]

        while lista_vars:
            print(lista_vars)
            for producao in self.regras[lista_vars[0]].derivados:
                if lista_vars[0] in tabela_passos[0]:
                    tabela_passos[0][lista_vars[0]].acrescenta_derivacao(
                        [BULLET] + producao + ['/0'])
                else:
                    tabela_passos[0][lista_vars[0]] = DerivacaoEarley([BULLET] + producao + ['/0'])
                if producao[0].isupper() and producao[0] not in lista_vars:
                    lista_vars += [producao[0]]
            lista_vars.pop(0)

        lista_simbolos = []
        for passo in range(1, tamanho_palavra + 1):
            print(tabela_passos)
            tabela_passos.append({})
            for chave, valor in tabela_passos[passo - 1].items():
                for producao in valor.derivados:
                    if producao[producao.index(BULLET) + 1] == palavra[passo - 1]:
                        if chave in tabela_passos[passo]:
                            move_ponto(producao)
                            tabela_passos[passo][chave].acrescenta_derivacao(producao)
                        else:
                            move_ponto(producao)
                            tabela_passos[passo][chave] = DerivacaoEarley(producao)
                            # print(producao)
                        lista_simbolos += [producao[producao.index(BULLET) + 1]]
                        if '/' in producao[producao.index(BULLET) + 1]:
                            lista_simbolos += [chave]
                        print(lista_simbolos)
            while lista_simbolos:
                # print(lista_simbolos)
                if lista_simbolos[0].isupper():
                    for producao in self.regras[lista_simbolos[0]].derivados:
                        if lista_simbolos[0] in tabela_passos[passo]:
                            nova_producao = [BULLET] + producao + ['/' + str(passo)]
                            tabela_passos[0][lista_simbolos[0]].acrescenta_derivacao(nova_producao)
                        else:
                            nova_producao = [BULLET] + producao + ['/' + str(passo)]
                            tabela_passos[0][lista_simbolos[0]] = DerivacaoEarley(nova_producao)
                        lista_simbolos += [nova_producao[nova_producao.index(BULLET) + 1]]
                        if '/' in nova_producao[nova_producao.index(BULLET) + 1]:
                            lista_simbolos += [lista_simbolos[0]]
                if '/' in lista_simbolos[0]:
                    # print(lista_simbolos[0])
                    passo_prod_final = int(lista_simbolos[0][1:])
                    for chave, valor in tabela_passos[passo_prod_final].items():
                        for producao in valor.derivados:
                            if producao[producao.index(BULLET) + 1] == lista_simbolos[1]:
                                if chave in tabela_passos[passo]:
                                    move_ponto(producao)
                                    tabela_passos[passo][chave].acrescenta_derivacao(producao)
                                else:
                                    move_ponto(producao)
                                    tabela_passos[passo][chave] = DerivacaoEarley(producao)
                                lista_simbolos += [producao[producao.index(BULLET) + 1]]
                                if '/' in producao[producao.index(BULLET) + 1]:
                                    lista_simbolos += [chave]
                    lista_simbolos.pop(0)
                lista_simbolos.pop(0)
            # print(tabela_passos)

    def __gera_nome_variavel_terminal(self, terminal):
        return 'TER' + terminal

    def __gera_nome_variavel_agrupamento(self, variaveis):
        return 'VAR' + '_'.join(variaveis)

    def __fecho_transitivo(self, fecho_variaveis, variavel, inicial):
        for producao in self.regras[variavel].derivados:
            if len(producao) == 1 and producao[0].isupper() and producao[0] not in fecho_variaveis[inicial]:
                fecho_variaveis[inicial].append(producao[0])
                # print(producao[0])
                fecho_variaveis[inicial] = self.__fecho_transitivo(
                    fecho_variaveis, producao[0], inicial)
        return fecho_variaveis[inicial]

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
                for chave, valor in copia_auxiliar_reg.items():
                    if variavel in valor.variaveis_geradas:
                        self.regras[chave].remove_derivacao_considerando_variavel(variavel)

        fecho_atingivel_terminais = []
        for chave, valor in self.regras.items():
            if valor.gera_terminal():
                fecho_atingivel_terminais.append(chave)
        for variavel in fecho_atingivel_terminais:
            fecho_atingivel_terminais += list(set(self.__fecho_indireto(variavel)
                                                  ) - set(fecho_atingivel_terminais))

        fecho_atingivel_variaveis = [self.inicial]
        for variavel in fecho_atingivel_variaveis:
            # print(fecho_atingivel_variaveis)
            for variavel_gerada in self.regras[variavel].variaveis_geradas:
                if variavel_gerada not in fecho_atingivel_variaveis:
                    fecho_atingivel_variaveis.append(variavel_gerada)

        diferenca_variaveis = [
            var for var in self.variaveis if var not in fecho_atingivel_variaveis]
        if diferenca_variaveis:
            for variavel in diferenca_variaveis:
                self.variaveis.remove(variavel)
                if variavel in self.regras:
                    self.regras.pop(variavel, None)

        diferenca_terminais = [
            var for var in self.variaveis if var not in fecho_atingivel_terminais]
        if diferenca_terminais:
            for variavel in diferenca_terminais:
                self.variaveis.remove(variavel)
                if variavel in self.regras:
                    self.regras.pop(variavel, None)
                for chave, valor in self.regras.items():
                    if variavel in valor.variaveis_geradas:
                        self.regras[chave].remove_derivacao_considerando_variavel(variavel)

    def __rep_dict(self):
        string = ''
        for key, value in self.regras.items():
            string += key + ' -> ' + str(value) + '\n'
        return string


def move_ponto(regra):
    index_ponto = regra.index(BULLET)
    regra[index_ponto], regra[index_ponto + 1] = regra[index_ponto + 1], regra[index_ponto]
