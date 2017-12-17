import os
import sys
from src.gramatica import Gramatica

entrada = Gramatica(os.path.abspath(sys.argv[1]))

print('----------Entrada----------\n', entrada)

entrada.simplificar()

print('--------Simplificada-------\n', entrada)

entrada.chomsky()

print('----------Chomsky----------\n', entrada)

#print('----------Earley-----------')
#print('Palavra:', sys.argv[2])
#derivavel = entrada.earley(sys.argv[2])

# if derivavel:
#
