from util.manage_files import read
from util.tokenizer import tokenizer
from collections import Counter

def categorizar(text:str):
    
    model      = read('prob')
    tokens     = Counter(tokenizer(text))
    categorias = model['p_categorias'].keys()

    test = {}

    for categoria in categorias:
        score = model['p_categorias'][categoria]
        for palavra, valor in model['p_palavras'][categoria].items():
            score *= tokens[palavra] * valor if palavra in tokens else valor
        test[categoria] = score

    categoria_final = ""
    categoria_score = 0
    for categoria in categorias:
        if test[categoria] > categoria_score:
            categoria_final = categoria
            categoria_score = test[categoria]

    return categoria_final