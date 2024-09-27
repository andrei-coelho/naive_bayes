from unidecode import unidecode

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


def escreveNoIndex(palavras_normalizadas:list[str]):
