from typing import Union, List
import json

def write(file:str, content):
    try:
        with open(f'modelo/{file}.json', 'w') as arquivo:
            json.dump(content, arquivo, indent=4)
            return True
    except FileNotFoundError:
        print(f"O arquivo {file}.json não foi encontrado.")
        return False
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON.")
        return False

def read(file:str):
    try:
        with open(f'modelo/{file}.json', 'r') as arquivo:
            jsonMap = json.load(arquivo)
        return jsonMap
    except FileNotFoundError:
        print(f"O arquivo {file}.json não foi encontrado.")
        return False
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON.")
        return False

def update(file: str, content, search: List[Union[str, int]] = None):
    
    jsonMap = read(file)

    if not jsonMap:
        return False

    if search is not None:
        objAtual = jsonMap
        for k in search:
            if k in objAtual:
                objAtual = objAtual[k]
            else:
                print(f"A chave {k} não foi encontrada.")
                return False

        objAtual.update(content)

    return write(file, objAtual)



