import os
import sys
from src.gramatica import Gramatica

entrada = Gramatica(os.path.abspath(sys.argv[1]))

print(entrada)
