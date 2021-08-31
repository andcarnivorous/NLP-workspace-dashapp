import base64

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from models.plotting import Plotter
from global_components.utils import make_output_toast
from utils import df_to_table
from word_frequency.word_frequency import app
from models.word_frequency_model import WordFrequencyModel


def make_box(id='upload-data', store="memory1", store_json="memory-df-json-tab-1", multiple=False):
    upload_box = html.Div([dcc.Store(store), dcc.Store(store_json),
                           dcc.Upload(
                               id=id, max_size=8e+6,
                               children=html.Div([
                                   'Drag and Drop or ',
                                   html.A('Select Files')
                               ], style={'display': 'inline-block'}),
                               style={
                                   'height': '50px',
                                   'lineHeight': '60px',
                                   'borderWidth': '1px',
                                   'borderStyle': 'dashed',
                                   'borderRadius': '5px',
                                   'textAlign': 'center',
                                   'margin-top': '1%',
                                   "width": "40%",
                               },
                               # Allow multiple files to be uploaded
                               multiple=multiple
                           )])
    return upload_box


def make_download_button_tab2():
    return html.Div(
        [
            dbc.Button("Download CSV", id="btn_csv_tab2", color="dark"),
            dcc.Download(id="download-dataframe-csv-tab2"),
        ]
    )


def make_download_button_tab1():
    return html.Div(
        [
            dbc.Button("Download CSV", id="btn_csv_tab1", color="dark"),
            dcc.Download(id="download-dataframe-csv-tab1"),
        ]
    )


def concordance_limit_slider():
    slider = html.Div([html.H5("LIMIT:"), dcc.Slider(min=2, max=10, step=1, value=2, id="slider-concordance", marks={
i: str(i) for i in range(2, 11)})])
    return slider


def make_ngram_slider_tab1():
    slider = html.Div([html.H5("NGRAMS:"), dcc.Slider(min=1, max=3, step=1, value=0, id="slider-ngrams-tab1", marks={
        1: '1',
        2: '2',
        3: '3',
    })])
    return slider


def make_ngram_slider_tab2():
    slider = html.Div(dcc.Slider(min=0, max=3, step=1, value=0, id="slider-ngrams-tab2", marks={
        0: '0',
        1: '1',
        2: '2',
        3: '3',
    }))
    return slider


@app.callback(
    Output('memory1', 'data'),
    [Input('upload-data', 'contents')] +
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')], prevent_initial_call=True
)
def update_upload(list_of_contents, list_of_names, list_of_dates):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "upload-data" in changed_id:
        if list_of_contents:
            list_of_contents = [list_of_contents]
            if len(list_of_contents) == 1:
                contents = list_of_contents[0]
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string).decode("utf-8")
                return [decoded]
            if len(list_of_contents) > 1:
                content_strings = [cont.split(",")[1] for cont in list_of_contents]
                content_strings = [base64.b64decode(content_string).decode("utf-8") for content_string in
                                   content_strings]
                content_strings = " ".join(content_strings)
                return [content_strings]
            return []
        return []
    return []


@app.callback(Output('upload-data', 'children'),
              [Input('upload-data', 'contents')] +
              [State('upload-data', 'filename'), State('upload-data', 'last_modified')])
def upload_box(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None and len(list_of_contents) == 1:
        contents = list_of_contents
        return html.P(f"{list_of_names}")
    elif list_of_contents is not None and len(list_of_contents) > 1:
        list_of_names = " ".join(list_of_names)
        return html.P(f"{list_of_names}")
    return html.Div(['Drag and Drop or ', html.A('Select Files')])


@app.callback(
    [Output("output-data-upload", "children"), Output("token-stats-toasts", "children"),
     Output("memory-df-json-tab-1", "data")],
    [Input('memory1', 'data'), Input("switches-input", "value"), Input("send-button", "n_clicks"),
     Input("card-tabs", "active_tab"),
     Input("input_len", "value"), Input("extra-stopwords", "value"), Input("slider-ngrams-tab1", "value")],
    prevent_initial_call=True,
)
def update_file_processing(text, switches_input, n_clicks, active_tab, length, extra_stopwords, ngrams):
    if active_tab == "tab-1":
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if "send-button" in changed_id:
            if not text:
                return dbc.Alert("You haven't uploaded files yet!", color="danger"), [], []
            ngrams = int(ngrams) if ngrams else 0
            length = int(length) if length else 10
            stopwords = True if "stopwords" in switches_input else False
            punct = True if "punct" in switches_input else False
            stem = True if "stem" in switches_input else False
            text = text[0] if len(text) > 0 else None
            if extra_stopwords:
                extra_stopwords = extra_stopwords.lower().split()
                extra_stopwords = extra_stopwords if extra_stopwords else []
            if not text:
                return dbc.Alert("You haven't uploaded files yet!", color="danger"), [], []
            wordfreq = WordFrequencyModel(text, extra_stopwords, stopwords, stem, punct, ngrams=ngrams)
            freq = wordfreq.frequencies(length)
            token_stats = wordfreq.tokens_stats()
            toasts = [make_output_toast("Unique Tokens:", str(len(token_stats[0]))),
                      make_output_toast("Avg Token Length:", "%.2f" % token_stats[1]),
                      make_output_toast("Longest token:", token_stats[2])]
            return html.Div([df_to_table(freq)]), toasts, wordfreq.df_to_json(freq)
        return [], [], []
    return [], [], []


@app.callback(
    Output("memory", "data"),  # Output("token-stats-toasts", "children")],
    [Input('textarea-example', 'value'), Input("switches-input", "value"), Input("input_len", "value"),
     Input("send-button", "n_clicks"), Input("card-tabs", "active_tab"), Input("extra-stopwords", "value"),
     Input("slider-ngrams-tab1", "value")],
    prevent_initial_call=True,
)
def update_output(text, switches_input, length, n_clicks, active_tab, extra_stopwords, ngrams):
    if active_tab == "tab-2":
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if not text:
            return dbc.Alert("There is no text!", color="danger")
        if len(text) > 10000:
            return dbc.Alert("Text is too long!", color="danger")

        if "send-button" in changed_id:
            length = int(length) if length else 10
            ngrams = int(ngrams) if ngrams else 0
            stopwords = True if "stopwords" in switches_input else False
            punct = True if "punct" in switches_input else False
            stem = True if "stem" in switches_input else False
            if extra_stopwords:
                extra_stopwords = extra_stopwords.lower().split()
                extra_stopwords = extra_stopwords if extra_stopwords else []
            wordfreq = WordFrequencyModel(text, extra_stopwords, stopwords, stem, punct, ngrams=ngrams)
            freq = wordfreq.frequencies(length)
            token_stats = wordfreq.tokens_stats()
            toasts = [make_output_toast(str(len(token_stats[0])), ""), make_output_toast(token_stats[1], ""),
                      make_output_toast(token_stats[2], "")]
            return wordfreq.df_to_json(freq)  # , toasts
        return []
    return []


@app.callback(
    Output('textarea-example-output', 'children'),
    [Input("input_len", "value"),
     Input("send-button", "n_clicks"), Input("memory", "data")],
    prevent_initial_call=True
)
def update_table(length, n_clicks, data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if "send-button" in changed_id:
        if isinstance(data, dict) and data["props"]["children"] == 'There is no text!':
            return dbc.Alert("There is no text!", color="danger")
        df = pd.read_json(data)
        return df_to_table(df)


@app.callback(
    Output("output-data-plot", "children"),
    [Input("plot-button", "n_clicks"), Input("memory-df-json-tab-1", 'data'), Input("card-tabs", "active_tab")],
    prevent_initial_call=True
)
def update_plot(n_clicks, data_tab1, active_tab):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "plot-button" in changed_id and data_tab1:
        if active_tab == "tab-1":
            df = pd.read_json(data_tab1)
            fig = Plotter(df, "Token", "Frequency", kind="bar").bar(title="Bar Chart")
            return dcc.Graph(id="chart", figure=fig,
                             style={  # 'display': 'block',
                                 # 'height': 600,
                                 # 'width': 900,
                                 'margin-left': 'auto',
                                 'margin-right': 'auto'})


@app.callback(
    Output("output-data-plot2", "children"),
    [Input("plot-button", "n_clicks"), Input("memory", "data"), Input("card-tabs", "active_tab")],
    prevent_initial_call=True
)
def update_plot2(n_clicks, data_tab2, active_tab):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "plot-button" in changed_id:  # and data_tab2["props"]["children"] != 'There is no text!':
        if active_tab == "tab-2":
            df = pd.read_json(data_tab2)
            fig = Plotter(df, "Token", "Frequency", kind="bar").bar(title="Bar Chart")
            return dcc.Graph(id="chart", figure=fig,
                             style={'display': 'block',
                                    # 'height': 600,
                                    # 'width': 900,
                                    'margin-left': 'auto',
                                    'margin-right': 'auto'})


@app.callback(
    Output("download-dataframe-csv-tab1", "data"),
    [Input("btn_csv_tab1", "n_clicks"), Input("memory-df-json-tab-1", "data"), Input("send-button", "n_clicks")],
    prevent_initial_call=True
)
def download_tab1(n_clicks, data, sent):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if data and "btn_csv_tab1" in changed_id and sent:
        df = pd.read_json(data)
        return dcc.send_data_frame(df.to_csv, "mydf.csv")


@app.callback(
    Output("download-dataframe-csv-tab2", "data"),
    [Input("btn_csv_tab2", "n_clicks"), Input("memory", "data"), Input("send-button", "n_clicks")],
    prevent_initial_call=True
)
def download_tab2(n_clicks, data, sent):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data and "btn_csv_tab2" in changed_id and sent:
        df = pd.read_json(data)
        return dcc.send_data_frame(df.to_csv, "mydf.csv")
