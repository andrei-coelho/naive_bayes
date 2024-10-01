from src.gerador_de_modelo import genTFIDF, genCategoriasPalavras, gerarTabelaProbabilidade
from src.modelo_classificador import categorizar

def main():
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

main()