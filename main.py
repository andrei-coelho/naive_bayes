from src.gerador_de_modelo import genTFIDF, genCategoriasPalavras, gerarTabelaProbabilidade

def main():
    rows = [
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
    ]
    total_rows = len(rows)
    categorias = genCategoriasPalavras(rows)
    # print(categorias)
    tfidf = genTFIDF(categorias)
    gerarTabelaProbabilidade(categorias, tfidf, total_rows)


main()