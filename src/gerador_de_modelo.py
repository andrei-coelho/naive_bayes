from collections import Counter
from util.manage_files import write, read
from util.mysqli import mysqli
from util.tokenizer import tokenizer

import random
import math


def getData():

    query = """
        SELECT nome, categoria FROM produtos
    """

    db = mysqli.instance()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(query)
        results = cursor.fetchall() 
        return results
    except Exception as e:
        print(f"Erro no banco de dados: {e}")
        return False

    
def genCategoriasPalavras(rows:list):
    
    categorias:dict[list] = {}

    for row in rows:

        nome      = row["nome"]
        categoria = row["categoria"]
        palavras  = Counter(tokenizer(nome))

        if not categoria in categorias:
            categorias[categoria] = []

        categorias[categoria].append({
            "doc":nome,
            "palavras":palavras
        })

    return categorias
    

def genIndexPalavras(categorias:dict):

    index:dict = {
        "total_registros":0,
        "palavras":{}
    }

    contagem_total_palavras = {}

    for categoria in categorias.keys():
        for palavra in categorias[categoria].keys():
            if palavra in contagem_total_palavras.keys():
                contagem_total_palavras[palavra] += categorias[categoria][palavra]
            else:
                contagem_total_palavras[palavra] = categorias[categoria][palavra]

    index["palavras"] = contagem_total_palavras
    return index
    

def genTFIDF(categorias:dict):
    
    TF  = {}

    categorias_nomes = categorias.keys()
    total_categorias = len(categorias_nomes)
    palavras_unicas  = []

    for categoria in categorias_nomes:
        
        total_por_termos = {}
        total_de_termos  = 0
        
        for doc in categorias[categoria]:
            for palavra in doc['palavras'].keys():
                if not palavra in palavras_unicas:
                    palavras_unicas.append(palavra)
                if not palavra in total_por_termos:
                    total_por_termos[palavra] = 0
                    total_de_termos += 1
                total_por_termos[palavra] += doc['palavras'][palavra]

        TF[categoria] = total_por_termos
        TF[categoria]['__total__'] = total_de_termos

    contagem_palavras_em_categorias = {}

    for categoria in categorias_nomes:
        palavras_cat = TF[categoria].keys()
        for palavra in palavras_unicas:
            if palavra in palavras_cat:
                if not palavra in contagem_palavras_em_categorias:
                    contagem_palavras_em_categorias[palavra] = 0
                contagem_palavras_em_categorias[palavra] += 1

    TF_IDF_palavras = {}
    TF_IDF_filtrado = {}

    for categoria in categorias_nomes:
        total_tf = TF[categoria]['__total__']

        for palavra in TF[categoria].keys():
            if palavra == '__total__': continue
            tf  = TF[categoria][palavra] / total_tf
            idf = total_categorias / contagem_palavras_em_categorias[palavra]
            if not categoria in TF_IDF_palavras:
                TF_IDF_palavras[categoria] = {}
            TF_IDF_palavras[categoria][palavra] = tf * idf

    for categoria, palavras_scores in TF_IDF_palavras.items():
        palavras_ordenadas = sorted(palavras_scores.items(), key=lambda x: x[1], reverse=True)
        TF_IDF_filtrado[categoria] = dict(palavras_ordenadas[:4])

    return ( TF_IDF_filtrado, TF )


def gerarTabelaProbabilidade(categorias:dict, tfidf, total_rows:int):
    
    TF_IDF_filtrado = tfidf[0]
    TF = tfidf[1]

    categorias_nomes = categorias.keys()
    total_docs = 0
    palavras_index = []
    total_docs_cat = {}
    tabela = {
        "p_categorias":{},
        "p_palavras":{}
    }

    for categoria in categorias_nomes:
        tabela['p_categorias'][categoria] = len(categorias[categoria]) / total_rows
        palavras = TF_IDF_filtrado[categoria].keys()
        for palavra in palavras:
            if not palavra in palavras_index:
                palavras_index.append(palavra)
    
    for categoria in categorias_nomes:
        tot = len(categorias[categoria])
        total_docs_cat[categoria] = tot
        total_docs += tot
  
    for categoria in categorias_nomes:
        for palavra in palavras_index:
            if not categoria in tabela['p_palavras']:
                tabela['p_palavras'][categoria] = {}
            if not palavra in TF[categoria] or not palavra in TF_IDF_filtrado[categoria]:
                tabela['p_palavras'][categoria][palavra] = 0.01
                continue
            tabela['p_palavras'][categoria][palavra] = math.log(((TF[categoria][palavra] / total_docs_cat[categoria]) * TF_IDF_filtrado[categoria][palavra]) + 1) 
    
    return tabela if write('tf_idf', TF_IDF_filtrado) and write('prob', tabela) else False

    

def test(text:str, categoria:str):
    pass

def training():

    rows = getData()
    if not rows:
        return None

    random.shuffle(rows)

    split_point   = int(0.8 * len(rows))
    training_data = results[:split_point]
    testing_data  = results[split_point:]
    
    categorias = genCategoriasPalavras(training_data)
    tfidf      = genTFIDF(categorias)

    tabela     = gerarTabelaProbabilidade(categorias, tfidf, len(training_data))

    


    
