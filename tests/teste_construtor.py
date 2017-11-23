import os
from src.gramatica import Gramatica

gramatica_teste = Gramatica(os.path.abspath('bin/grammar.txt'))

print(gramatica_teste)
