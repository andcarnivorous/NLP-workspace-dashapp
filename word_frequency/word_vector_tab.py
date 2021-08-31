import base64

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from word_frequency.word_frequency import app
from models.word_vector_model import WordVectorModel


def make_update_vector():
    return dcc.Loading(id="output-data-upload-vector")


def make_plot_vector():
    return html.Div([dcc.Loading(id="output-data-plot-vector")])


def make_box_vector():
    upload_box = html.Div([dcc.Upload(
        id='upload-data-vector', max_size=7e+6,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '33%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            "margin-top": 50
        },
        # Allow multiple files to be uploaded
        multiple=True
    ), dcc.Store("memory-vector"), dcc.Store("memory-df-json-tab-vector")])
    return upload_box


def plotting_button_vector():
    plot_button = html.Div(
        dbc.Button('Scatter Plot', id='plot-button-vector', n_clicks=0, color="secondary", className="mr-222"))
    return plot_button


@app.callback(
    Output('memory-vector', 'data'),
    [Input('upload-data-vector', 'contents')] +
    [State('upload-data-vector', 'filename'), State('upload-data-vector', 'last_modified')], prevent_initial_call=True)
def update_upload(list_of_contents, list_of_names, list_of_dates):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "upload-data-vector" in changed_id:
        if list_of_contents:
            if len(list_of_contents) == 1:
                contents = list_of_contents[0]
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string).decode("utf-8")
                return [decoded]
            if len(list_of_contents) > 1:
                content_strings = [cont.split(",")[1] for cont in list_of_contents]
                content_strings = [base64.b64decode(content_string).decode("utf-8") for content_string in content_strings]
                content_strings = " ".join(content_strings)
                return [content_strings]
        return []


@app.callback(Output('upload-data-vector', 'children'),
              [Input('upload-data-vector', 'contents')] +
              [State('upload-data-vector', 'filename'), State('upload-data-vector', 'last_modified')])
def upload_box(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None and len(list_of_contents) == 1:
        contents = list_of_contents[0]
        return html.P(f"{list_of_names[0]}")
    elif list_of_contents is not None and len(list_of_contents) > 1:
        list_of_names = " ".join(list_of_names)
        return html.P(f"{list_of_names}")
    else:
        return html.Div(['Drag and Drop or ', html.A('Select Files')])


@app.callback(
    [Output("output-data-plot-vector", "children"), Output("memory-df-json-tab-vector", "data")],
    [Input('memory-vector', 'data'), Input("plot-button-vector", "n_clicks"), Input("card-tabs", "active_tab")],
    prevent_initial_call=True
)
def update_file_processing(text, n_clicks, active_tab):
    if active_tab == "tab-4":
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if "plot-button-vector" in changed_id and n_clicks < 5 and text:
            model = WordVectorModel(text[0])
            fig = model.PCA_plotter.plot()
            return_value = dcc.Graph(figure=fig,
                                     style={'display': 'block',
                                            'height': 1200,
                                            'width': 1800,
                                            'margin-left': 'auto',
                                            'margin-right': 'auto'})
            return return_value, model.df_to_json(model.df)
        if "plot-button-vector" in changed_id and not text:
            return dbc.Alert("You haven't uploaded files yet!", color="danger"), []
        return [], []
    return [], []


def make_download_button_vector():
    return html.Div(
        [
            dbc.Button("Download CSV", id="btn_csv_vector"),
            dcc.Download(id="download-dataframe-csv-vector"),
        ]
    )


@app.callback(
    Output("download-dataframe-csv-vector", "data"),
    [Input("btn_csv_vector", "n_clicks"), Input("memory-df-json-tab-vector", "data"),
     Input("plot-button-vector", "n_clicks")],
    prevent_initial_call=True
)
def download_tab_vectors(n_clicks, data, sent):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data and "btn_csv_vector" in changed_id and sent:
        df = pd.read_json(data)
        return dcc.send_data_frame(df.to_csv, "mydf.csv")
