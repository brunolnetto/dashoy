import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.core.constants import GEOMARCADORES, DELIMITADOR_SOJA, ENCODING_SOJA

def obter_geodados_soja(
    df_: pd.DataFrame
):
    estados, regioes, regioes_economicas, pais = obter_geolocalizacoes(df_)
    anos = obter_anos(df_)
    
    uf_marcador = df_.columns[0]
    
    mascara_tem_2 = df_[uf_marcador].str.len() == 2
    
    eh_regiao = df_[uf_marcador].isin(regioes)
    eh_eregiao = df_[uf_marcador].isin(regioes_economicas)
    eh_pais = df_[uf_marcador].isin(pais)
    
    mascara_uf = mascara_tem_2
    mascara_regiao = eh_regiao
    mascara_eregiao = eh_eregiao
    mascara_brasil = eh_pais

    df_soja_estados = df_[mascara_uf]
    df_soja_regiao = df_[mascara_regiao]
    df_soja_eregiao = df_[mascara_eregiao]
    df_soja_pais = df_[mascara_brasil]
    
    uf_regiao = ['UF']+anos
    coluna_regiao = ['region']+anos
    coluna_eregiao = ['eregion']+anos
    coluna_pais = ['country']+anos

    df_soja_estados.columns = uf_regiao
    df_soja_regiao.columns = coluna_regiao
    df_soja_eregiao.columns = coluna_eregiao
    df_soja_pais.columns = coluna_pais
    
    return df_soja_estados, df_soja_regiao, df_soja_eregiao, df_soja_pais
    
def tentar_conversao_float_coalescer_zero(
    valor: str
):
    valor = str(valor).strip()
    return 0 if valor == '-' else float(valor)
    
def obter_marcador_serie(
    df_: pd.DataFrame, 
    marcador: list
):
    coluna_descritiva = df_.columns[0]
    coluna_nao_descritiva = df_.columns[1:]
    mascara_marcador = df_[coluna_descritiva] == marcador
    
    df_marcador = df_[mascara_marcador]
    
    valores = []
    for _, linha in df_marcador.iterrows():
        valores = [
            tentar_conversao_float_coalescer_zero(linha[col])
            for col in coluna_nao_descritiva
        ]
    
    return valores
    
def obter_marcadores_serie(
    df_: pd.DataFrame, 
    marcadores: list
):
    
    return {
        marcador: obter_marcador_serie(df_, marcador) 
        for marcador in marcadores
    } 

def obter_anos(
    df_: pd.DataFrame
):
    return [
        int(year.split('/')[0]) 
        for year in df_.columns[1:]
    ]

def obter_geolocalizacoes(
    df_: pd.DataFrame
):
    uf_marcador = df_.columns[0]
    
    mascara_tem_2 = df_[uf_marcador].str.len() == 2
    mascara_nao_tem_2 = df_[uf_marcador].str.len() != 2
    
    lista_regioes = list(df_[mascara_nao_tem_2][uf_marcador])
    
    estados = list(df_[mascara_tem_2][uf_marcador])
    regioes = lista_regioes[0:5]
    regioes_economicas = lista_regioes[5:7]
    pais = [lista_regioes[7]]
    
    return estados, regioes, regioes_economicas, pais

def carregar_dados_soja(
    rota_absoluta_arquivo: str
):
    return pd.read_csv(
        rota_absoluta_arquivo, 
        delimiter=DELIMITADOR_SOJA, 
        encoding=ENCODING_SOJA
    )

def transpor_geodados_soja(df_: pd.DataFrame):
    df_ = df_.copy(deep=True)
    
    # 1. Seta coluna nao numerica como index
    geo_index=[
        col 
        for col in df_.columns 
        if not isinstance(col, int)
    ][0]
    
    df_.set_index(geo_index, inplace=True)
    
    # 2. Transpoem DataFrame
    df_ = df_.transpose()
    
    # 3. Reseta indice
    df_.reset_index(inplace=True)
    
    # 4. Renomea 'UF' para 'anos'
    df_.rename(columns={'index': 'anos'}, inplace=True)
    
    df_.columns.name = None

    return df_

def montar_geodados_soja(
    geodado: pd.DataFrame, 
    geomarcadores: list
):
    df_geodados_soja = transpor_geodados_soja(geodado)
    
    return {
        'dataframe': df_geodados_soja,
        'dict': obter_marcadores_serie(geodado, geomarcadores)
    }

def montar_dados_soja(
    df_: pd.DataFrame
):
    return {
        geo_marcador: montar_geodados_soja(geodado, geolocalizacao)
        for geo_marcador, 
            geodado, 
            geolocalizacao in zip(
            GEOMARCADORES, 
            obter_geodados_soja(df_), 
            obter_geolocalizacoes(df_)
        )
    }

def validar_nome_arquivo(
    fname: str
):
    splitted_fname = fname.split('.')
    return splitted_fname[-1].lower() == 'csv'

def validar_nomes_arquivos(
    nome_arquivos: list
):
    from numpy import where, array
    
    validation_arr = []
    
    for nome_arquivo in nome_arquivos:
        validation_arr.append(validar_nome_arquivo(nome_arquivo))

    are_false = array(validation_arr) == False
    are_false_indexes = list(where(are_false)[0])
    
    if(len(are_false_indexes) != 0):
        false_elems = [nome_arquivos[index] for index in are_false_indexes]

        false_msg = '\n'.join(false_elems)
        error_message = f'Arquivos abaixo são inválidos:\n{false_msg}'
        
        raise ValueError(error_message)

def obter_dados_soja(
    rota_origem: str, 
    nome_arquivos: list
):
    validar_nomes_arquivos(nome_arquivos)

    dados_soja = dict()
    
    for nome_arquivo in nome_arquivos:
        df_soja = carregar_dados_soja(rota_origem+nome_arquivo)
        rota_arquivo = rota_origem+nome_arquivo
        chave_ = nome_arquivo.split('.')[0]

        dados_soja[chave_] = {
            'dataframe': df_soja, 
            'tempo': obter_anos(df_soja), 
            'geodados': montar_dados_soja(df_soja)
        }

    return dados_soja

def obter_geodados_por_geomarcador(dados_dict: dict, geomarcador: str):
    dados_chaves = dados_dict.keys()

    geodados_lista = []
    for dados_coluna in dados_chaves:
        df_ = dados_dict[dados_coluna]['geodados'][geomarcador]['dataframe']
        geodados_lista.append(df_ )

    return geodados_lista

def plotar_geodados_interativo_soja(
    geodados_lista: list,
    titulo:str, subplot_titles: list, ylabels: list,
    eh_empilhado: bool = True
):
    
    # Create subplots
    fig = make_subplots(rows=1, cols=3, subplot_titles=subplot_titles)
    
    # Add stacked area plots to subplots
    for idx, geodados_elem in enumerate(geodados_lista):
        data_labels = [
            col 
            for col in geodados_elem.columns 
            if col != 'anos'
        ]

        for enum_val, data_label in enumerate(data_labels):
            if eh_empilhado:
                fill_label = 'tozeroy' if enum_val == 0 else 'tonexty'
            else:
                fill_label = 'tozeroy'
            
            x = geodados_elem['anos']
            y = geodados_elem[data_label]

            scatter_data = go.Scatter(
                x=x, y=y, 
                fill= fill_label, name=data_label, stackgroup='one'
            )

            fig.update_xaxes(title_text='Tempo [anos]', row=1, col=idx+1)
            fig.update_yaxes(title_text=ylabels[idx], row=1, col=idx+1)
            fig.add_trace(scatter_data, row=1, col=idx+1)

    # Update layout
    fig.update_layout(showlegend=True, hovermode='x', title=titulo)
    
    # Show plot
    fig.show()

def plotar_dados_soja(
    marcador: str, 
    x: np.ndarray, 
    y_dict: dict, 
    y_marcador: str
):
    
    plt.figure(figsize=(10, 8))

    # Stacked area plot
    plt.title('Acumulada')
    plt.stackplot(x, y_dict.values(), labels=y_dict.keys())

    plt.xlabel('Tempo [Anos]')
    plt.ylabel(y_marcador)
    plt.legend(title='Legend', loc='upper left')

    plt.suptitle(f'{y_marcador} por {marcador}')
    plt.tight_layout()
    plt.show()