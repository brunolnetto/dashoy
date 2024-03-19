import pandas as pd

from plotly.subplots import make_subplots
from urllib.request import urlopen
import shutil
from zipfile import ZipFile
import plotly.graph_objects as go
import os
from os import listdir
import re


from src.utils.type_utils import igualdade_string_relaxada, normalizar_numeros    
from src.core.constants import (
    GEOMARCADORES,
    DELIMITADOR_CLIMA,
    ENCODING_CLIMA,
    CLIMA_COLUNAS_DADOS,
    CLIMA_METRICS,
    ESTADOS_PARA_REGIAO,
    ESTADOS_PARA_EREGIAO,
    SIGLAS_PARA_ESTADOS,
    COLUNA_TEMPERATURA,
    COLUNA_PRECIPITACAO,
    DELIMITADORES_TEMPO
)

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
    with ZipFile(file_path, 'r') as zip_ref:
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

def obter_arquivos_csv_clima(rota_clima):
    from os import listdir
    arquivos_clima = listdir(rota_clima)
    
    return [
        arquivo_clima
        for arquivo_clima in arquivos_clima
        if igualdade_string_relaxada(
            arquivo_clima.split('.')[-1], 
            'csv'
        )
    ] 

def obter_uf_pelo_arquivo_clima(climate_file_):
    return climate_file_.split('_')[2]

def obter_ufs_pela_rota_base(rota_clima):
    arquivos_clima = obter_arquivos_csv_clima(rota_clima)
    
    return list(
        {
            obter_uf_pelo_arquivo(arquivo_clima) 
            for arquivo_clima in arquivos_clima
        }
    )

def obter_anos_pela_rota_base(rota_clima):
    return [int(ano) for ano in listdir(rota_clima)]

def normalizar_dataframe_clima(df_):
    str_para_float = lambda x: float(str(x).replace(',', '.'))
    normalizar_str = lambda x: float(str_para_float(normalizar_numeros(str(x))))
    
    df_[COLUNA_TEMPERATURA] = df_[COLUNA_TEMPERATURA].apply(str_para_float)
    df_[COLUNA_PRECIPITACAO] = df_[COLUNA_PRECIPITACAO].apply(normalizar_str)

    precipitacao_has_9999_float = df_[COLUNA_PRECIPITACAO] > 0
    temperatura_has_9999_float = df_[COLUNA_TEMPERATURA] > -50

    cleanse_mask = precipitacao_has_9999_float & temperatura_has_9999_float
        
    return df_[cleanse_mask]

def obter_dados_clima(rota_fonte, skiprows=8):
    df_ = pd.read_csv(
        rota_fonte, 
        skiprows=skiprows,  
        delimiter=DELIMITADOR_CLIMA, 
        encoding=ENCODING_CLIMA
    )
    
    # Reset the index
    df_.reset_index(drop=True, inplace=True)
    
    return normalizar_dataframe_clima(df_)

def adicionar_ano_a_dataframe_clima(df_: pd.DataFrame):
    df = df_.copy()  # Create a copy of the DataFrame
    col_tempo = df_.columns[0]
    split_map = lambda x: float(
        re.split('|'.join(
            map(
                re.escape, DELIMITADORES_TEMPO)
            ), 
            str(x)
        )[0]
    )
    df['ano'] = df_[col_tempo].apply(split_map)
    
    return df

def adicionar_mes_a_dataframe_clima(df_: pd.DataFrame):
    df = df_.copy()  # Create a copy of the DataFrame
    col_tempo = df_.columns[0]
    split_map = lambda x: float(re.split('|'.join(map(re.escape, DELIMITADORES_TEMPO)), str(x))[1])
    df['mes'] = df_[col_tempo].apply(split_map)
    
    return df

def adicionar_uf_a_dataframe_clima(
    df_: pd.DataFrame,
    uf_clima: str
):
    df_['UF'] = uf_clima
    df_len = len(df_.columns)
    columns = list(df_.columns)
    colunas_novas = cherry_place(columns, df_len-1, 2)
    df_ = df_[colunas_novas]
    
    return df_

def remover_coluna_unnamed(
    df_: pd.DataFrame
):
    coluna_unnamed = [ 
        col
        for col in df_.columns
        if col.lower().find('unnamed') != -1
    ][0]
    
    df_.drop(coluna_unnamed, axis=1)

    return df_

def transformar_dataframe_clima(
    df_: pd.DataFrame,
    arquivo_clima: str
):
    uf_clima = obter_uf_pelo_arquivo_clima(arquivo_clima)
    df_ = adicionar_uf_a_dataframe_clima(df_, uf_clima)
    
    df_ = adicionar_ano_a_dataframe_clima(df_)
    df_ = adicionar_mes_a_dataframe_clima(df_)
    remover_coluna_unnamed(df_)
    
    return df_

def agrupar_dataframe_clima(
    df_: pd.DataFrame
):
    col_precipitacao = CLIMA_COLUNAS_DADOS[0]
    col_temperatura = CLIMA_COLUNAS_DADOS[1]
    
    colunas_grupo = ['ano', 'UF']
    
    # Use the metrics dictionary in the groupby aggregation
    result = df_.groupby(colunas_grupo).agg(CLIMA_METRICS)
    
    # Flatten the column index
    result.columns = ['_'.join(col).strip() for col in result.columns.values]
    
    result = result.reset_index()
    
    return result


def obter_sumario_regiao_clima(
    df_estados: pd.DataFrame    
):
    df_regiao = df_estados.copy()
    para_regiao = lambda x: ESTADOS_PARA_REGIAO[x]
    df_regiao['UF'] = df_regiao['UF'].apply(para_regiao)

    return agrupar_dataframe_clima(df_regiao)

def obter_sumario_eregiao_clima(
    df_estados: pd.DataFrame    
):
    df_eregiao = df_estados.copy()
    para_eregiao = lambda x: ESTADOS_PARA_EREGIAO[x]
    df_eregiao['UF'] = df_eregiao['UF'].apply(para_eregiao)

    return agrupar_dataframe_clima(df_eregiao)

def obter_sumario_pais_clima(
    df_estados: pd.DataFrame    
):
    df_pais = df_estados.copy()
    df_pais['UF'] = 'Brasil'

    return agrupar_dataframe_clima(df_pais)

def obter_sumario_geoclima(
    df_estados: pd.DataFrame
):
    dataframes_clima = (
        agrupar_dataframe_clima(df_estados), \
        obter_sumario_regiao_clima(df_estados), \
        obter_sumario_eregiao_clima(df_estados), \
        obter_sumario_pais_clima(df_estados)
    )

    geo_dataframes_zip = zip(GEOMARCADORES, dataframes_clima)
    return dict(geo_dataframes_zip)

def plotar_dados_clima(
    df_: pd.DataFrame,
    geolabel: str
):
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=('Rain Quantity', 'Temperature')
    )
    
    # Rain Quantity subplot
    dados_chuva = {
        'x': df_['ano'], 
        'y': df_['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)_sum'], 
        'marker_color': 'blue'
    }
    
    bar = go.Bar(dados_chuva)
    
    fig.add_trace(bar, row=1, col=1)
    fig.update_xaxes(title_text='Year', row=1, col=1)
    fig.update_yaxes(title_text='Rain Quantity (mm) - ', row=1, col=1)
    
    # Temperature subplot with error bars
    x = df_['ano']
    y = df_['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)_mean']
    median = df_['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)_median']
    q1 = df_['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)_quantile1']
    q3 = df_['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)_quantile3']
    error_values = dict(type='data', symmetric=False, array=median-q1, arrayminus=q3-median)
    
    dados_temperatura = {
        'x': x,
        'y': y,
        'error_y': error_values,
        'mode':'lines+markers', 
        'marker_color':'red', 
        'name':'Mean Temperature'
    }
    
    scatter = go.Scatter(dados_temperatura)
    
    fig.add_trace(scatter, row=1, col=2)
    fig.update_xaxes(title_text='Year', row=1, col=2)
    fig.update_yaxes(title_text='Temperature (°C)', row=1, col=2)
    
    fig.update_layout(
        title=f'Precipitação e Temperatura - {geolabel}', 
        showlegend=False
    )
    fig.show()

def plotar_estado_clima(
        df_orig: pd.DataFrame, 
        geolabel: str
    ):
    mask = df_orig['UF'] == geolabel
    df = df_orig[mask]
    
    geolabel = SIGLAS_PARA_ESTADOS[geolabel]
    
    plotar_dados_clima(df, geolabel)