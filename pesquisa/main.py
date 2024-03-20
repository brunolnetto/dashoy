

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen
import zipfile
import shutil
import tqdm

URL_DADOS_CLIMA = 'https://portal.inmet.gov.br/uploads/dadoshistoricos/'
ANOS_CLIMA = list(range(2000, 2025))

def percorrer_e_mover_pastas(pasta_raiz, eh_verbose=False):
    # Obter a lista de todas as subpastas
    subpastas = [f.path for f in os.scandir(pasta_raiz) if f.is_dir()]
    
    # Percorrer cada subpasta
    for subpasta in subpastas:
        # Usar a subpasta como nova pasta raiz
        percorrer_e_mover_pastas(subpasta)
        
        # Obter a lista de todos os arquivos na subpasta
        arquivos = [f.path for f in os.scandir(subpasta) if f.is_file()]
        
        # Mover cada arquivo para a pasta raiz atual
        for caminho_arquivo in arquivos:
            nome_arquivo = os.path.basename(caminho_arquivo)
            novo_caminho_arquivo = os.path.join(pasta_raiz, nome_arquivo)
            # Check if the file already exists in the destination directory
            if os.path.exists(novo_caminho_arquivo):
                # Rename the file
                nome_arquivo, extensao = os.path.splitext(nome_arquivo)
                contador = 1
                while True:
                    novo_nome_arquivo = f"{nome_arquivo}_{contador}{extensao}"
                    novo_caminho_arquivo = os.path.join(pasta_raiz, novo_nome_arquivo)
                    if not os.path.exists(novo_caminho_arquivo):
                        break
                    contador += 1

                if(eh_verbose):
                    print(f"Arquivo renomeado para {novo_nome_arquivo}")
            
            # Move the file to the destination directory
            shutil.move(caminho_arquivo, novo_caminho_arquivo)
            
            if(eh_verbose):
                print(f"Arquivo movido de {caminho_arquivo} para {novo_caminho_arquivo}")
        
        # Remover a subpasta
        os.rmdir(subpasta)
        if(eh_verbose):
            print(f"Subpasta removida: {subpasta}")

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

def tarefa_obter_dados_clima(url, folder_path, ano):
    file_name = f'{ano}.zip'
    file_folder = folder_path+'/'+file_name.split('.')[0] 
    
    download_e_salvar_zip(url, folder_path, file_name)

    file_folder = os.path.join(folder_path, f'{ano}')
    percorrer_e_mover_pastas(file_folder)

folder_path = os.path.join(os.getcwd(), 'data', 'clima')

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

with ThreadPoolExecutor() as executor:
    futures = []
    for ano in ANOS_CLIMA:
        file_name = str(ano) + '.zip'
        url = URL_DADOS_CLIMA + file_name
        futures.append(
            executor.submit(
                tarefa_obter_dados_clima, 
                url, folder_path, ano
            )
        )
    
    # Use tqdm to create a progress bar
    for future in tqdm(
        as_completed(futures), 
        total=len(futures), 
        desc="Downloading files"
    ):
        future.result()  # Wait for the download to complete