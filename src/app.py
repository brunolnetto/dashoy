import dash
import plotly.express as px
from dash.dependencies import Input, Output

import numpy as np

from core.setup import setup_app 
from callbacks.callbacks import update_dropdown_b_options, \
    update_plot 

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the options for the dropdowns
options = {
    'A': ['A1', 'A2', 'A3'],
    'B': ['B1', 'B2'],
    'C': ['C1', 'C2', 'C3', 'C4']
}

app = setup_app(app, options)

# Set the callback functions
@app.callback(
    Output('dropdown-b', 'options'),
    Input('dropdown-a', 'value')
)
def update_dropdown_b(selected_option):
    return update_dropdown_b_options(selected_option, options)

@app.callback(
    Output('plot', 'figure'),
    Input('dropdown-a', 'value'),
    Input('dropdown-b', 'value')
)
def update_plot_callback(selected_option_a, selected_option_b):
    return update_plot(selected_option_a, selected_option_b)

@app.callback(
    Output('option-div', 'className'),
    Input('dropdown-a', 'value')
)
def update_option_div_class(selected_option):
    return f"option-div option-{selected_option.lower()}"

if __name__ == '__main__':
    app.run_server(debug=True)