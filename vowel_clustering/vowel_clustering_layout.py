import dash_bootstrap_components as dbc
import dash_html_components as html
from vowel_clustering.vowel_clustering import app
from dash.dependencies import Input, Output
import dash_core_components as dcc

from vowel_clustering.configs import models, columns
from global_components.menu import navbar
from global_components.utils import display_page
from vowel_clustering.clustering_callbacks import make_box, make_params, make_update, confirmation_button

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

base = html.Div([
    navbar,
    html.Div([
        dbc.Jumbotron([
            html.H1("Unsupervised Clustering of Vowels",
                    className="display-3"),
            html.H2(
                "Insert your vowel's dataset and perform clustering",
                className="lead",
            )])]),
    html.H5("Choose two different columns:"),
    html.Div([
        dbc.RadioItems(id="column1",
                       options=columns,
                       value='F1',
                       labelStyle={'display': 'inline-block'}, inline=True)]),
    html.Div([
        dbc.RadioItems(id="column2",
                       options=columns,
                       value='F2',
                       labelStyle={'display': 'inline-block'}, inline=True)]),
    html.H5("Choose a model:", style={"margin-top": 50}),
    html.Div([
        dbc.RadioItems(id="model-type",
                       options=models,
                       value='DBSCAN',
                       labelStyle={'display': 'inline-block'}, inline=True),
        make_params(), html.Div([confirmation_button(), dbc.Button('?', id='info-button', n_clicks=0, color="dark",
                                                                   style={"border-radius": "50%"})], className="row")
    ]),
    html.Hr(),
    html.Center(make_box()),
    html.Center(
        html.P("Use column names F1, F2, F3, F4 in the files you want to process.")),
    html.Hr(),
    html.Div(make_update()),
    html.Div(id='output-data-table')])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display(pathname):
    return display_page(pathname, "vowel", base)
