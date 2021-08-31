import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from flask import abort

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])


def make_info_toast(header: str, text: str):
    return dbc.Toast(
        [html.P(text, className="mb-0")],
        id="simple-toast",
        header=header,
        icon="info",
        dismissable=True,
    )


def make_output_toast(header: str, text: str):
    return dbc.Toast(
        [html.P(text, className="mb-0")],
        id="simple-toast",
        header=header,
        icon="success",
        dismissable=False, style={'display': 'inline-block'}
    )


def display_page(pathname, page, base):
    if pathname == f'/{page}/':
        return base
    else:
        return abort(404)
