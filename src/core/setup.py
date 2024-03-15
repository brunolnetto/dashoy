import dash
from dash import html, dcc
from utils.toml_utils import get_authors

def get_main_content(options):
    option_div = html.Div(
        [
            html.Label("Select option A, B, or C:"),
            dcc.Dropdown(
                id='dropdown-a',
                options=[{'label': k, 'value': k} for k in options.keys()],
                value='A',
                style={'width': '50%', 'margin': 'auto'}
            )
        ],
        className='option-div',
        style={'text-align': 'center'}
    )

    suboption_div = html.Div(
        [
            html.Label("Select sub-option:"),
            dcc.Dropdown(
                id='dropdown-b',
                value=options['A'][0],
                style={'width': '50%', 'margin': 'auto'}
            )
        ], style={'text-align': 'center'}
    )
    
    graph = dcc.Graph(id='plot', style={'margin': 'auto', 'width': '50%'})

    main_content_components = [option_div, suboption_div, graph]
    return html.Div(
        main_content_components, 
        className='main-content', 
        style={'max-width': '800px', 'margin': 'auto'}
    )

def get_footer():
    return html.Div(
        className='footer', 
        children=[
            html.P(
                "Powered by Dash", 
                className='footer-text')
        ]
    )

def get_header(title):
    return html.Div([
        html.H1(
            title, 
            className='header-title'
        ),
        html.P(
            f"Desenvolvido por {get_authors()}", 
            className='header-text'
        )
    ], className='header')

def setup_app(app: dash.Dash, title: str, options: dict):
    css_link = html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    )

    header = get_header(title)
    main_content = get_main_content(options)
    footer = get_footer()

    div_content = [
        css_link,
        header,
        main_content,
        footer
    ]

    # Define the layout of the app
    app.layout = html.Div(div_content)

    return app
