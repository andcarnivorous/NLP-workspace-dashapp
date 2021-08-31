main_module_code = """
#  This module creates the instance of the Home page.


from utils import generate_app

app = generate_app(__name__, url_base_pathname='/%s/')"""

layout_module_code = """import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from global_components.menu import navbar
from global_components.utils import display_page
from %s.%s import app

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

base = html.Div([navbar])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display(pathname):
    return display_page(pathname, "%s", base)"""
