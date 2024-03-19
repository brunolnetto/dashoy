import os
from urllib.request import urlopen
import zipfile
import requests
import re
import xlrd

def baixar_e_salvar_arquivo_xls(
    url: str, 
    pasta_destino: str,
    nome_arquivo: str
):
    # Cria a pasta se ela não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Obtém o nome do arquivo a partir da URL
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    
    # Baixa o arquivo
    resposta = requests.get(url)
    if resposta.status_code == 200:
        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
            
        print(f"Arquivo baixado e salvo em: {caminho_arquivo}")

        # Verifica se é um arquivo XLS ou XLSX usando regex
        if re.search(r'\.xls[x]?$', nome_arquivo):
            # Abre o arquivo XLS
            workbook = xlrd.open_workbook(caminho_arquivo)
            # Exemplo de como você pode processar o conteúdo do arquivo XLS
            for sheet_name in workbook.sheet_names():
                sheet = workbook.sheet_by_name(sheet_name)
                
    else:
        print(f"Falha ao baixar o arquivo: {resposta.status_code}")

def download_e_salvar_zip(url, folder_path, file_name, eh_verbose=False):
    # Cria a pasta se ela não existir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Caminho completo do arquivo
    file_path = os.path.join(folder_path, file_name)
    
    # Baixa o arquivo
    with urlopen(url) as response, open(file_path, 'wb') as file:
        file.write(response.read())
    
    if(eh_verbose):
        print(f"Arquivo ZIP baixado e salvo em: {file_path}")
    
    # Extrai o arquivo
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Obtém o nome da pasta para extrair o conteúdo do arquivo
        folder_name = os.path.splitext(file_name)[0]
        extract_path = os.path.join(folder_path, folder_name)
        
        zip_ref.extractall(extract_path)
    
    if(eh_verbose):
        print(f"Conteúdo do arquivo ZIP extraído em: {extract_path}")
    
    # Deleta o arquivo ZIP
    os.remove(file_path)
    if(eh_verbose):
        print(f"Arquivo ZIP deletado: {file_path}")