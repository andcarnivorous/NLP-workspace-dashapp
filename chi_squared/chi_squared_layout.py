import dash_bootstrap_components as dbc
import dash_html_components as html

from global_components.layout import Layout
from global_components.menu import navbar
#from word_frequency.word_frequency_callbacks import make_box
from global_components.utils import make_info_toast, display_page
from chi_squared.chi_squared_callbacks import make_box
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from chi_squared.chi_squared import app

layout_instance = Layout(preprocessing={"Remove Stopwords": "stopwords",
                                        "Apply Stemming": "stem"},
                         buttons={"confirmation": ["Send", "send-button"],
                                  "download": ["Download", "download-button"]})

tokens_to_match = dbc.InputGroup([dbc.InputGroupAddon("Token To Match:", addon_type="prepend"),
                                  dbc.Input(id="input-1", placeholder="Token To Match", type="text", maxLength=30,
                                            style={"width": "30%"}),
                                  ], style={"margin-bottom": "1%", "width": "30%"})

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

base = html.Div([navbar,
                 html.Div([
                     html.Div([make_info_toast("How to Use",
                                               "Choose a word/token, upload the corpora files you want to test "
                                               "the word/token against, press the Send button to perform a chi-squared "
                                               "test on the corpora you uploaded."),
                               make_box("upload-file-1", store="memory1", store_json="memory-df-json-tab-1",
                                        multiple=True)],
                              style={'width': '40%', 'display': 'inline-block', "margin-bottom": "1%"}),
                     tokens_to_match,
                     layout_instance.preprocessing,
                     html.Div([dbc.ButtonGroup([layout_instance.buttons["confirmation"], layout_instance.buttons["download"]])],
                              style={'width': '100%', 'display': 'inline-block', "margin-bottom": "3%"}),
                     html.Div(id="chi-table"), html.Div(id="test"), dcc.Store("memory-output"),
                     dcc.Download("download-output")
                 ])])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display(pathname):
    return display_page(pathname, "chi_squared", base)
