import dash
from dash import html, dcc
from utils.toml_utils import get_authors

def setup_app(app: dash.Dash, options: dict):
    css_link = html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    )
    header = html.Div([
        html.H1(
            "Análise sobre produção de soja", 
            className='header-title'
        ),
        html.P(
            f"Desenvolvido por {get_authors()}", 
            className='header-text'
        )
    ], className='header')
    option_div = html.Div(
        [
            html.Label("Select option A, B, or C:"),
            dcc.Dropdown(
                id='dropdown-a',
                options=[{'label': k, 'value': k} for k in options.keys()],
                value='A'
            )
        ],
        className='option-div'
    )
    suboption_div = html.Div(
        [
            html.Label("Select sub-option:"),
            dcc.Dropdown(
                id='dropdown-b',
                value=options['A'][0]
            )
        ]
    )
    graph = dcc.Graph(id='plot')

    footer = html.Div(
        className='footer', 
        children=[
            html.P(
                "Powered by Dash", 
                className='footer-text')
        ]
    )

    div_content = [
        css_link,
        header,
        option_div,
        suboption_div,
        graph,
        footer
    ]

    # Define the layout of the app
    app.layout = html.Div(div_content)

    return app
