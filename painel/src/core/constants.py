from urllib.request import urlopen

from src.utils.type_utils import inverter_dicionario
from src.utils.statistics_utils import quantile1, median, quantile3

GITHUBUSERCONTENT_URL = 'https://raw.githubusercontent.com'
ROTA_GEOMETRIA_BRASIL = '/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
URL_GEOMETRIA_BRASIL = f'{GITHUBUSERCONTENT_URL}{ROTA_GEOMETRIA_BRASIL}'

# Source: 
# https://python.plainenglish.io/ ...
# how-to-create-a-interative-map-using-plotly-express-geojson-to-brazil-in-python-fb5527ae38fc
def obter_geometria_brasil():
    from json import load 
    
    with urlopen(URL_GEOMETRIA_BRASIL) as response:
        return load(response)
    
    return Brazil 

def obter_uf_para_estado(Brazil):
    state_id_map = {}
    for feature in Brazil['features']:
        feature['id'] = feature['properties']['name']
        sigla = feature['properties']['sigla']
        state_id_map[sigla] = feature['id']
    
    return state_id_map

def obter_regiao_para_estado():
    return {
        'NORTE': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
        'NORDESTE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'CENTRO-OESTE': ['DF', 'GO', 'MT', 'MS'],
        'SUL': ['PR', 'RS', 'SC'],
        'SUDESTE': ['ES', 'MG', 'RJ', 'SP']
    }

def obter_estado_para_regiao():
    return inverter_dicionario(obter_regiao_para_estado())

def obter_eregiao_para_estado():
    return {
    'NORTE/NORDESTE': [
        'AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO', 'AL', 
        'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'
    ],
    'CENTRO-SUL': [
        'DF', 'GO', 'MT', 'MS', 'PR', 
        'RS', 'SC', 'ES', 'MG', 'RJ', 'SP'
    ]
}

def obter_estado_para_eregiao():
    return inverter_dicionario(obter_eregiao_para_estado())

GEOLABELS = [
    [
        'AC', 'AP', 'AM', 'PA', 'RO', 'RR', 
        'TO', 'AL', 'BA', 'CE', 'MA', 'PB', 
        'PE', 'PI', 'RN', 'SE', 'DF', 'GO', 
        'MT', 'MS', 'PR', 'RS', 'SC', 'ES', 
        'MG', 'RJ', 'SP'
    ],
    ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUL', 'SUDESTE'],
    [ 'CENTRO-SUL', 'NORTE/NORDESTE' ]
]

GEOMETRIA_BRAZIL = obter_geometria_brasil()

REGIAO_PARA_ESTADOS = obter_regiao_para_estado()
ESTADOS_PARA_REGIAO = obter_estado_para_regiao()
EREGIAO_PARA_ESTADOS = obter_eregiao_para_estado()
ESTADOS_PARA_EREGIAO = obter_estado_para_eregiao()
SIGLAS_PARA_ESTADOS = obter_uf_para_estado(GEOMETRIA_BRAZIL)

CLIMA_COLUNAS_TEMPO = [
    'DATA (YYYY-MM-DD)', 'Data'
]

CLIMA_COLUNAS_DADOS = [
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'
]

COLUNA_PRECIPITACAO = CLIMA_COLUNAS_DADOS[0]
COLUNA_TEMPERATURA = CLIMA_COLUNAS_DADOS[1]

CLIMA_METRICS = {
    COLUNA_PRECIPITACAO: 'sum',
    COLUNA_TEMPERATURA: ['mean', 'std', quantile1, median, quantile3, 'min', 'max']
}

DELIMITADORES_TEMPO = ['-', '/']
DELIMITADOR_CLIMA = ';'
DELIMITADOR_SOJA = ','

ENCODING_SOJA = 'utf8'
ENCODING_CLIMA = 'latin-1'

ANOS_CLIMA = list(range(2000, 2025))

GEOMARCADORES = [
    'Estados', 'Regiões políticas', 'Regiões econômicas', 'País'
]

SOJA_MARCADORES = GEOMARCADORES
CLIMA_MARCADORES = dict(zip(GEOMARCADORES, GEOLABELS))

# URL do arquivo a ser baixado
URL_DADOS_SOJA = "https://www.conab.gov.br/info-agro/safras/serie-historica-das-safras/item/download/52220_02561b9dfaf9252623ee9876f592aaf4"
URL_DADOS_CLIMA = 'https://portal.inmet.gov.br/uploads/dadoshistoricos/'