from src.gerador_de_modelo import *
from src.modelo_classificador import *

def testIntegrado():
    rows = [
        {
            "nome": "palavra1 palavra2 e palavra3",
            "categoria": "categoria1"
        },
        {
            "nome": "palavra1 palavra2 e palavra2",
            "categoria": "categoria2"
        },
        {
            "nome": "palavra1 palavra3 e palavra3",
            "categoria": "categoria1"
        },
        {
            "nome": "palavra1 palavra3 e palavra2",
            "categoria": "categoria1"
        },
        {
            "nome": "palavra4 palavra2 e palavra2",
            "categoria": "categoria2"
        },
        {
            "nome": "palavra1 palavra2 e palavra2",
            "categoria": "categoria2"
        },
        {
            "nome": "palavra3 palavra4 e palavra1",
            "categoria": "categoria3"
        },
        {
            "nome": "palavra4 palavra3 e palavra2",
            "categoria": "categoria3"
        },
        {
            "nome": "palavra2 palavra4 e palavra3",
            "categoria": "categoria3"
        },
        {
            "nome": "palavra2 palavra3 e palavra1",
            "categoria": "categoria1"
        },
    ]

    training_data = rows[:8]
    testing_data  = rows[8:]

    total_rows = len(training_data)
    categorias = genCategoriasPalavras(training_data)
    tfidf = genTFIDF(categorias)
    gerarTabelaProbabilidade(categorias, tfidf, total_rows)

    for item in testing_data:
        categoria = categorizar(item['nome'])
        print(categoria == item['categoria'])


def testGenCategoriasPalavras():
    categorias = genCategoriasPalavras([
        {
            "nome":"palavra1 palavra2 e palavra3",
            "categoria":"categoria1",
        },
        {
            "nome":"palavra1 palavra2 e palavra2",
            "categoria":"categoria2",
        },
        {
            "nome":"palavra1 palavra3 e palavra3",
            "categoria":"categoria1",
        }
    ])
    print(categorias['categoria1'][0]['palavras']['palavra1']==1)
    print(categorias['categoria1'][1]['palavras']['palavra3']==2)


def testGenIndexPalavras():
    index = genIndexPalavras({
        'categoria1': [
            {
                'doc': 'palavra1 palavra2 e palavra3', 
                'palavras': {
                    'palavra1': 1, 
                    'palavra2': 1, 
                    'palavra3': 1
                }
            }, 
            {
                'doc': 'palavra1 palavra3 e palavra3', 
                'palavras': {
                    'palavra3': 2, 
                    'palavra1': 1
                }
            }
        ], 
        'categoria2': [
            {
                'doc': 'palavra1 palavra2 e palavra2', 
                'palavras': {
                    'palavra2': 2, 
                    'palavra1': 1
                }
            }
        ]
    })
    print(index["palavras"]["palavra1"] == 6)
    print(index["palavras"]["palavra2"] == 4)
    print(index["palavras"]["palavra3"] == 9)



