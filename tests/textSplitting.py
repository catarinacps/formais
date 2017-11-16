import os

with open(os.path.abspath('resources/grammar.txt')) as textFile:
    raw = textFile.readlines()
    print(raw)
    for linha in raw:
        print(linha)