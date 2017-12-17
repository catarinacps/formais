import re
from collections import deque
from src.regras import *
from src.tree import *


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
        # Remocao das producaoes vazias
        fecho_vazio = []
        # Inicializamos o fecho vazio
        for chave, valor in self.regras.items():
            # e colocamos, inicialmente, todas as producoes de palavras vazias no fecho
            if valor.gera_vazio():
                fecho_vazio.append(chave)
        # após isso, achamos o fecho indireto de producoes que produzem tais variavel que produzem vazio
        for variavel in fecho_vazio:
            # e adicionamos todas as novas variaveis que produzem indiretamente o vazio
            fecho_vazio += list(set(self.__fecho_indireto(variavel)) - set(fecho_vazio))

        copia_auxiliar = self.regras.copy()
        for variavel, derivacao in copia_auxiliar.items():
            # Apos isso, removemos todas as derivacoes que produzem vazio da gramatica
            if variavel != self.inicial and derivacao.gera_vazio():
                if len(derivacao.derivados) == 1:
                    self.__remove_variavel(variavel)
                else:
                    self.regras[variavel].remove_derivacao([VAZIO])
        copia_auxiliar = self.regras.copy()
        for variavel, derivacao in copia_auxiliar.items():
            # E
            for gerador_vazio in fecho_vazio:
                if derivacao.gera_variavel(key=gerador_vazio):
                    self.regras[variavel].duplica_derivacoes(gerador_vazio)

        fecho_variaveis = {}
        for variavel in self.variaveis:
            fecho_variaveis[variavel] = []
            fecho_variaveis[variavel] = self.__fecho_transitivo(fecho_variaveis, variavel, variavel)

        for variavel in self.variaveis:
            novas_producoes = Derivacao()
            if variavel in self.regras:
                for producao in self.regras[variavel].derivados:
                    if len(producao) == 1 and producao[0].islower() and producao not in novas_producoes.derivados:
                        novas_producoes.acrescenta_derivacao(producao)
                    elif len(producao) >= 2 and producao not in novas_producoes.derivados:
                        novas_producoes.acrescenta_derivacao(producao)
            for var in fecho_variaveis[variavel]:
                if var in self.regras:
                    for producao in self.regras[var].derivados:
                        if len(producao) == 1 and producao[0].islower() and producao not in novas_producoes.derivados:
                            novas_producoes.acrescenta_derivacao(producao)
                        elif len(producao) >= 2 and producao not in novas_producoes.derivados:
                            novas_producoes.acrescenta_derivacao(producao)
            self.regras[variavel] = novas_producoes

        self.__remove_simbolos_inuteis()

    def chomsky(self):
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

        copia_auxiliar_reg = list(self.regras.items()).copy()
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
        """Implementacao do parser de earley em Python 3.

        Recenbendo a entrada a ser reconhecida, retorna no terminal cada passo do algoritmo e o
        resultado final.

        Arguments:
            palavra {string} -- Palavra a ser testada.
        """

        for terminal in palavra:
            if terminal not in self.terminais:
                print('Palavra possui um terminal que nao pertence a linguagem')
                return False
        if palavra == '':
            print('String \'palavra\' vazia. Para reconhecer a palavra vazia, utilize \'V\'')
            return False

        tamanho_palavra = len(palavra)
        word = DerivacaoEarley([BULLET] + list(palavra))

        # Tabela de passos, i.e. D0, D1, D2 e etc
        tabela_passos = []

        # Passo D0:

        # Inicializamos o D0 na chave do dicionario que corresponde a variavel inicial
        tabela_passos.append({self.inicial: DerivacaoEarley()})
        # Fila de variaveis a serem visitadas pelo algoritmo no passo D0
        fila_vars_apos_ponto = deque([])
        # Para todas as producoes da variavel inicial
        for producao in self.regras[self.inicial].derivados:
            # Nos acrescentamos elas no passo D0
            tabela_passos[0][self.inicial].acrescenta_derivacao([BULLET] + producao + ['/0'], Arvore(self.inicial), producao)
            # e, se o primeiro item da producao for uma variavel (ou seja, o item apos o ponto)
            if producao[0].isupper():
                # ele e adicionado na fila de afazeres, pois tal variavel deve ter suas producoes
                # adicionadas a D0 tambem
                fila_vars_apos_ponto.append(producao[0])

        # Enquanto ainda existir variaveis a serem adicionadas a D0
        while fila_vars_apos_ponto:
            var_atual = fila_vars_apos_ponto.popleft()
            # Visitaremos todas as producoes da dita variavel
            for producao in self.regras[var_atual].derivados:
                # Se essa variavel ja existir no passo atual
                if var_atual in tabela_passos[0]:
                    # simplesmente acresentamos a pordução
                    tabela_passos[0][var_atual].acrescenta_derivacao([BULLET] + producao + ['/0'])
                else:
                    # senao, inicializamos a variavel no passo atual
                    tabela_passos[0][var_atual] = DerivacaoEarley([BULLET] + producao + ['/0'])

                # Finalmente, se o simbolo apos o ponto e uma variavel e ainda nao foi visitada
                if producao[0].isupper() and producao[0] not in fila_vars_apos_ponto and producao[0] != var_atual:
                    # ela e adicionada a fila de afazeres
                    fila_vars_apos_ponto.append(producao[0])

        print('D0:', word)
        print('------------------------')
        print(self.__rep_passo(tabela_passos[0]))
        print('')

        # Passos Dr

        # Inicializamos a fila de simbolos a serem visitados
        fila_simbolos_apos_ponto = deque([])
        for passo in range(1, tamanho_palavra + 1):
            tabela_passos.append({})
            for chave, valor in tabela_passos[passo - 1].items():
                for producao in valor.derivados:
                    if producao[producao.index(BULLET) + 1] == palavra[passo - 1]:
                        nova_producao = producao.copy()
                        move_ponto(nova_producao)
                        simb_apos_ponto = nova_producao[nova_producao.index(BULLET) + 1]
                        # print(nova_producao)
                        if chave in tabela_passos[passo]:
                            tabela_passos[passo][chave].acrescenta_derivacao(nova_producao)
                        else:
                            tabela_passos[passo][chave] = DerivacaoEarley(nova_producao)

                        # Finalmente, se o simbolo apos o ponto e uma variavel e ainda nao foi visitada
                        if simb_apos_ponto.isupper() and simb_apos_ponto not in fila_simbolos_apos_ponto:
                            # ela e adicionada a fila de afazeres
                            fila_simbolos_apos_ponto.append(simb_apos_ponto)
                        if '/' in simb_apos_ponto:
                            if simb_apos_ponto not in fila_simbolos_apos_ponto and chave not in fila_simbolos_apos_ponto:
                                fila_simbolos_apos_ponto.append(simb_apos_ponto)
                                fila_simbolos_apos_ponto.append(chave)

            while fila_simbolos_apos_ponto:
                simb_atual = fila_simbolos_apos_ponto.popleft()
                if simb_atual.isupper():
                    for producao in self.regras[simb_atual].derivados:
                        nova_producao = [BULLET] + producao + ['/' + str(passo)]
                        simb_apos_ponto = nova_producao[nova_producao.index(BULLET) + 1]
                        if simb_atual in tabela_passos[passo]:
                            tabela_passos[passo][simb_atual].acrescenta_derivacao(nova_producao)
                        else:
                            tabela_passos[passo][simb_atual] = DerivacaoEarley(nova_producao)

                        # Finalmente, se o simbolo apos o ponto e uma variavel e ainda nao foi visitada
                        if simb_apos_ponto.isupper() and simb_apos_ponto not in fila_simbolos_apos_ponto and simb_apos_ponto != simb_atual:
                            # ela e adicionada a fila de afazeres
                            fila_simbolos_apos_ponto.append(simb_apos_ponto)

                if '/' in simb_atual:
                    passo_prod_final = int(simb_atual[1:])
                    var_prod_final = fila_simbolos_apos_ponto.popleft()

                    for chave, valor in tabela_passos[passo_prod_final].items():
                        for producao in valor.derivados:
                            if producao[producao.index(BULLET) + 1] == var_prod_final:
                                nova_producao = producao.copy()
                                move_ponto(nova_producao)
                                simb_apos_ponto = nova_producao[nova_producao.index(BULLET) + 1]
                                if chave in tabela_passos[passo]:
                                    tabela_passos[passo][chave].acrescenta_derivacao(nova_producao)
                                else:
                                    tabela_passos[passo][chave] = DerivacaoEarley(nova_producao)

                                # Finalmente, se o simbolo apos o ponto e uma variavel e ainda nao foi visitada
                                if simb_apos_ponto.isupper() and simb_apos_ponto not in fila_simbolos_apos_ponto:
                                    # ela e adicionada a fila de afazeres
                                    fila_simbolos_apos_ponto.append(simb_apos_ponto)
                                if '/' in simb_apos_ponto:
                                    if simb_apos_ponto != simb_atual and chave != var_prod_final:
                                        fila_simbolos_apos_ponto.append(simb_apos_ponto)
                                        fila_simbolos_apos_ponto.append(chave)
            move_ponto(word.derivados[0])
            print('D' + str(passo) + ':', word)
            print('------------------------')
            print(self.__rep_passo(tabela_passos[passo]))
            print('')

        if self.inicial in tabela_passos[-1]:
            for producao in tabela_passos[-1][self.inicial].derivados:
                simb_apos_ponto = producao[producao.index(BULLET) + 1]
                if '/' in simb_apos_ponto:
                    print('Reconhece a palavra \'' + palavra + '\'!')
                    return True
        print('Nao reconhece a palavra \'' + palavra + '\'!')
        return False

    def __gera_nome_variavel_terminal(self, terminal):
        return 'TERM_' + terminal.upper()

    def __gera_nome_variavel_agrupamento(self, variaveis):
        return 'VAR' + '_'.join(variaveis).upper()

    def __fecho_transitivo(self, fecho_variaveis, variavel, inicial):
        if variavel in self.regras:
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

    def __rep_passo(self, passo):
        string = ''
        for key, value in passo.items():
            for producao in value.lista_producoes():
                string += key + ' -> ' + producao + '\n'
        return string


def move_ponto(regra):
    index_ponto = regra.index(BULLET)
    regra[index_ponto], regra[index_ponto + 1] = regra[index_ponto + 1], regra[index_ponto]
