import pandas as pd
from src.utils.type_utils import remover_caracteres_especiais
import os

def extrair_sheets_de_arquivo_xls(nome_arquivo_soja, pasta_origem, pasta_destino, skip_rows=0):
    """
    Extrai cada planilha de um arquivo Excel e a salva como um arquivo CSV separado.

    Parâmetros:
    - nome_arquivo_soja (str): O nome do arquivo Excel.
    - pasta_origem (str): O caminho para a pasta contendo o arquivo Excel.
    - pasta_destino (str): O caminho para a pasta onde os arquivos CSV serão salvos.
    - skip_rows (int): Número de linhas a serem puladas no início de cada planilha (padrão é 0).
    """
    # Caminho para o arquivo Excel
    caminho_arquivo_excel = os.path.join(pasta_origem, nome_arquivo_soja)

    # Ler o arquivo Excel
    xls = pd.ExcelFile(caminho_arquivo_excel)

    # Obter os nomes das planilhas
    nomes_planilhas = xls.sheet_names

    # Criar a pasta de destino se ela não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Iterar sobre cada planilha e salvá-la como um arquivo CSV
    nomes_arquivos = []
    for nome_planilha in nomes_planilhas:
        df = pd.read_excel(caminho_arquivo_excel, sheet_name=nome_planilha, skiprows=skip_rows)

        nome_planilha_ = remover_caracteres_especiais(nome_planilha).lower()
        nome_arquivo = f'{nome_planilha_}_soja.csv'
        
        caminho_arquivo_csv = os.path.join(pasta_destino, nome_arquivo)
        
        df.to_csv(caminho_arquivo_csv, index=False)

        print(f'Planilha "{nome_planilha}" salva como arquivo CSV: {caminho_arquivo_csv}')

        nomes_arquivos.append(nome_arquivo)

    return nomes_arquivos
