import dash_bootstrap_components as dbc
import dash_html_components as html

download_button = html.Div(dbc.Button('Download', id='download-button', n_clicks=0, color="dark", className="mr-111"))


def confirmation_button(id='send-button'):
    confirm_button = html.Div(dbc.Button('Send', id=id, n_clicks=0, color="dark", className="mr-1"))
    return confirm_button


def plotting_button(id='plot-button'):
    plot_button = html.Div(dbc.Button('BarPlot', id=id, n_clicks=0, color="dark", className="mr-222"))
    return plot_button