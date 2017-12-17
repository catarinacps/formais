"""Usage:

program <operation> <file name>
        Where operation can be:
            fnc         -   Chomsky Normal Form
            earley      -   Parse a word with the Earley parser
            simplificar -   Simplify the grammar
"""


import os
import sys
from src.gramatica import Gramatica


try:
    if sys.argv[1] == 'fnc':
        entrada = Gramatica(os.path.abspath(sys.argv[2]))
        print('----------Entrada----------\n', entrada)
        entrada.simplificar()
        print('--------Simplificada-------\n', entrada)
        entrada.chomsky()
        print('----------Chomsky----------\n', entrada)
    elif sys.argv[1] == 'earley':
        entrada = Gramatica(os.path.abspath(sys.argv[2]))
        print('----------Entrada----------\n', entrada)
        entrada.simplificar()
        print('--------Simplificada-------\n', entrada)

        palavra = input('Palavra que deseja reconhecer (para sair, digite \'-q\'):')
        while palavra != '-q':
            print('----------Earley-----------')
            derivavel = entrada.earley(palavra)

            if derivavel:
                pass

            palavra = input('Palavra que deseja reconhecer (para sair, digite \'-q\'):')
    elif sys.argv[1] == 'simplificar':
        entrada = Gramatica(os.path.abspath(sys.argv[2]))
        print('----------Entrada----------\n', entrada)
        entrada.simplificar()
        print('--------Simplificada-------\n', entrada)
    elif sys.argv[1] == 'carregar':
        pass
        # entrada = Gramatica(os.path.abspath(sys.argv[2]))
        # print('----------Entrada----------\n', entrada)

        # operacao = input('Operacao que deseja realizar: ')
except IndexError:
    print('Parametros incorretos, por favor siga o seguinte funcionamento:')
    print(__doc__)
