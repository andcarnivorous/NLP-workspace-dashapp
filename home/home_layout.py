import dash_bootstrap_components as dbc
import dash_gif_component as gif
import dash_html_components as html
from flask import abort
from global_components.menu import navbar
import dash_core_components as dcc
from home.home import app
from dash.dependencies import Input, Output

with open("home/HOME.md") as home_md:
    home_md = home_md.read()

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

base = html.Div([
    navbar,
    dbc.Toast([html.H3("Does not look like it, but we are working for you...", style={"margin-top": "15px"}),
               gif.GifPlayer(autoplay=True,
                             gif='https://64.media.tumblr.com/d2b89f6876236bb34cb60bebb92620be/tumblr_nv48nctJwH1sbmu2ho2_250.gif',
                             still='https://64.media.tumblr.com/d2b89f6876236bb34cb60bebb92620be/tumblr_nv48nctJwH1sbmu2ho2_250.gif',
                             alt='loading', )
               ], style={"position": "fixed", "top": 66, "right": 10, "width": 350}, dismissable=True, duration=8000),
    html.Center([
        dcc.Markdown(home_md)  # , style={"width": "66%"})
    ])])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return base
    else:
        return abort(404)
