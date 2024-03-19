from locale import setlocale, atof, LC_ALL
from locale import str as locale_str
from warnings import warn

def igualdade_string_relaxada(str1: str, str2: str):
    return str1.lower() == str2.lower()

def normalizar_numeros(number_str):
    # Set the locale to the user's default locale
    setlocale(LC_ALL, '')
    
    # Parse the number-like string to a float
    number = atof(number_str)
    
    # Format the float back to a string using the user's locale
    normalized_number_str = locale_str(number)
    
    return normalized_number_str.replace(',', '.')

def remover_caracteres_especiais(texto):
    from unicodedata import normalize
    import re
    
    # Normalize the text to decomposed form
    text_normalizado = normalize('NFD', texto)
    
    # Use regex to remove non-alphanumeric characters and spaces
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s]', '', text_normalizado)
    
    # Remove extra spaces and return the cleaned text
    return ' '.join(texto_limpo.split())

def cherry_place(lst: list, from_index:int, to_index: int):
    # Remove element at index 2 (3) and store it in a variable
    element = lst.pop(from_index)

      # Insert the element at the specified index
    lst.insert(to_index, element)
    
    return lst

def inverter_dicionario(dicio: dict):
    dicio_novo = dict()
    
    for chave, valor in dicio.items():
        if(isinstance(valor, list)):
            for el in valor:
                chaves_dicio_novo = list(dicio_novo.keys())
                if(el in chaves_dicio_novo):
                    warn(f'Elemento {el} já tem chave associada {chaves_dicio_novo[el]}. ')
                else:
                    dicio_novo[el] = chave

        else:
            emsg = 'Todos valores do dicionário devem ser listas!'
            raise ValueError(emsg)

    return dicio_novo

def obter_chave_dict(ref_dict: dict, valor):
    candidatos = []
    
    for chave, lista_elementos in ref_dict.items():
        if(isinstance(lista_elementos, list)):
            if(valor in lista_elementos):
                candidatos.append(chave)
            else:
                continue
        else:
            emsg = 'Todos valores do dicionário-referencia devem ser listas!'
            raise ValueError(emsg)

    if(len(candidatos) == 0):
        return None
    if(len(candidatos) == 1):
        return candidatos[0]
    else:
        emsg = 'Apenas uma chave para valor fornecido deve existir!'
        raise ValueError(emsg)