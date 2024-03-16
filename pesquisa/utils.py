import json
from urllib.request import urlopen
import pandas as pd


# Source: 
# https://python.plainenglish.io/how-to-create-a-interative-map-using-plotly-express-geojson-to-brazil-in-python-fb5527ae38fc
def states_geojson():
    githubusercontent_url = 'https://raw.githubusercontent.com'
    route = '/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
    with urlopen(f'{githubusercontent_url}{route}') as response:
        Brazil = json.load(response)

    state_id_map = {}
    for feature in Brazil['features']:
        feature['id'] = feature['properties']['name']
        sigla = feature['properties']['sigla']
        state_id_map[sigla] = feature['id']

    return Brazil, state_id_map 