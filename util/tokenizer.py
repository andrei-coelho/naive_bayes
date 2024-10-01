import unicodedata
import re

stop_words = [
    "a", "ao", "aos", "aonde", "aquelas", "aquele", "aqueles", "aqui", "-",
    "as", "assim", "com", "como", "da", "das", "de", "delas", "dele", "+",
    "deles", "depois", "desde", "do", "dos", "e", "em", "entre", "era", "_",
    "esse", "essa", "esses", "essas", "eu", "havia", "ha", "i", "isso", "/",
    "isto", "ja", "la", "lhe", "lhes", "me", "meu", "meus", "na", "nas", "\\",
    "naquilo", "nao", "nem", "nas", "nisto", "nada", "nos", "o", "os", ",",
    "outro", "outros", "para", "pela", "pelas", "pelo", "pelos", "porem", ";",
    "que", "quem", "se", "seu", "seus", "sob", "sobre", "tanto", "tudo", "?",
    "um", "uma", "umas", "uns", "voce", "vos", "aonde", "adiante", "agora", "!",
    "ali", "alem", "antes", "entre", "enquanto", "hoje", "ja", "junto", ".",
    "mais", "menos", "mesmo", "nunca", "pouco", "sempre", "entao", "|"
]


def normalize(palavra: str) -> str:
    palavra = unicodedata.normalize('NFKD', palavra)
    return ''.join(c for c in palavra if unicodedata.category(c) != 'Mn').lower().strip()


def tokenizer(text:str):

    text     = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    palavras = text.split(" ")
    palavras_normalizadas = []

    for palavra in palavras:
        palavra = normalize(palavra)
        if palavra.strip() == "" or palavra in stop_words:
            continue
        palavras_normalizadas.append(palavra)
    
    return palavras_normalizadas