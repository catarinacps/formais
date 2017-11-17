import os
from src.gramatica import Gramatica

gramaticaTeste = Gramatica(os.path.abspath('bin/grammar.txt'))

print(gramaticaTeste)
