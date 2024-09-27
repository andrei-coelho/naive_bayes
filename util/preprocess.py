from unidecode import unidecode

def normalize(data:str):
    return unidecode(data).lower()

