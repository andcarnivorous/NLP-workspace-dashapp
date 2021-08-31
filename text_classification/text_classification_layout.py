import dash_html_components as html

from global_components.menu import navbar
from global_components.utils import display_page
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from text_classification.text_classification import app
from global_components.buttons import confirmation_button
import text_classification.text_classification_callbacks

textarea = dcc.Textarea(
    id='textarea-example',
    value='Textarea contenot initialized\nwith multiple lines of text',
    style={'height': 50, "width": "50%"},
)

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

base = html.Div([navbar, html.Div([textarea,
                                   confirmation_button(),
                                   html.Br(), html.Hr(),
                                   html.Center(html.Div(id="classification-output"))])])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display(pathname):
    return display_page(pathname, "text_classification", base)
