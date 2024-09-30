from collections import Counter
from src.manage_files import write, read
from util.mysqli import mysqli

import math
import unicodedata


stop_words = [
    "a", "ao", "aos", "aonde", "aquelas", "aquele", "aqueles", "aqui",
    "as", "assim", "com", "como", "da", "das", "de", "delas", "dele",
    "deles", "depois", "desde", "do", "dos", "e", "em", "entre", "era",
    "esse", "essa", "esses", "essas", "eu", "havia", "ha", "i", "isso",
    "isto", "ja", "la", "lhe", "lhes", "me", "meu", "meus", "na", "nas",
    "naquilo", "nao", "nem", "nas", "nisto", "nada", "nos", "o", "os",
    "outro", "outros", "para", "pela", "pelas", "pelo", "pelos", "porem",
    "que", "quem", "se", "seu", "seus", "sob", "sobre", "tanto", "tudo",
    "um", "uma", "umas", "uns", "voce", "vos", "aonde", "adiante", "agora",
    "ali", "alem", "antes", "entre", "enquanto", "hoje", "ja", "junto",
    "mais", "menos", "mesmo", "nunca", "pouco", "sempre", "entao"
]

def normalize(palavra: str) -> str:
    palavra = unicodedata.normalize('NFKD', palavra)
    return ''.join(c for c in palavra if unicodedata.category(c) != 'Mn').lower()


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


def tokenizer(text:str):

    palavras = text.split(" ")
    palavras_normalizadas = []

    for palavra in palavras:
        palavra = normalize(palavra)
        if palavra in stop_words:
            continue
        palavras_normalizadas.append(palavra)
    
    return palavras_normalizadas


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
        palavras = TF_IDF_filtrado[categoria].keys()
        for palavra in palavras:
            if not palavra in palavras_index:
                palavras_index.append(palavra)
    
    for categoria in categorias_nomes:
        tot = len(categorias[categoria])
        total_docs_cat[categoria] = tot
        total_docs += tot

    print(total_docs_cat)

    # print(categorias)
    # print(TF_IDF_filtrado)
    # print(TF)

    for categoria in categorias_nomes:
        for palavra in palavras_index:
            if not categoria in tabela['p_palavras']:
                tabela['p_palavras'][categoria] = {}
            if not palavra in TF[categoria]:
                tabela['p_palavras'][categoria][palavra] = 0.01
                continue
            tabela['p_palavras'][categoria][palavra] = math.log(((TF[categoria][palavra] / total_docs_cat[categoria]) * TF_IDF_filtrado[categoria][palavra]) + 1) 

    print(tabela)


def genModel():

    rows = getData()
    total_rows = len(rows)
    if not rows:
        return None

    categorias = genCategoriasPalavras(rows)

    print(categorias)
    
    