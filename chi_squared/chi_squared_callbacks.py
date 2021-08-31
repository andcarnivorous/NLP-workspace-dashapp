import base64

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from utils import df_to_table
from chi_squared.chi_squared import app
from models.chi_squared_model import ChiSquared


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


@app.callback(
    Output('memory1', 'data'),
    [Input('upload-file-1', 'contents')] +
    [State('upload-file-1', 'filename'), State('upload-file-1', 'last_modified')], prevent_initial_call=True
)
def update_upload(list_of_contents, list_of_names, list_of_dates):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "upload-file-1" in changed_id:
        if list_of_contents:
            if len(list_of_contents) == 1:
                contents = list_of_contents[0]
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string).decode("utf-8")
                return {list_of_names[0]: decoded}
            if len(list_of_contents) > 1:
                content_strings = [cont.split(",")[1] for cont in list_of_contents]
                content_strings = [base64.b64decode(content_string).decode("utf-8") for content_string in
                                   content_strings]
                content_strings_dict = {list_of_names[idx]: content_strings[idx] for idx in range(len(content_strings))}
                return content_strings_dict
    return []


@app.callback(Output('upload-file-1', 'children'),
              [Input('upload-file-1', 'contents')] +
              [State('upload-file-1', 'filename'), State('upload-file-1', 'last_modified')])
def upload_box(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None and len(list_of_contents) == 1:
        return html.P(f"{list_of_names[0]}")
    elif list_of_contents is not None and len(list_of_contents) > 1:
        list_of_names = " ".join(list_of_names)
        return html.P(f"{list_of_names}")
    return html.Div(['Drag and Drop or ', html.A('Select Files')])


@app.callback(
    [Output("memory-output", "data"), Output("test", "children"), Output("chi-table", "children")],
    [Input('memory1', 'data'), Input("switches-input", "value"), Input("send-button", "n_clicks"),
     Input("input-1", "value")],
    prevent_initial_call=True
)
def update_file_processing(text_dict, switches_input, n_clicks, test_word):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "send-button" in changed_id and test_word:
        text_dict = text_dict
        stopwords = True if "stopwords" in switches_input else False
        stem = True if "stem" in switches_input else False
        chi_squared_model = ChiSquared(text_dict, test_word, stopwords, stem)
        chi2, p, dof, expected, table = chi_squared_model.calculate_chi_square()
        df = pd.DataFrame(table, columns=list(text_dict.keys()))
        df.insert(0, "", [test_word.upper(), "Rest of Words"])
        table = df_to_table(df)
        toasts = html.Div(
            [dbc.Toast([html.P(f"{p}")], header="P-value", style={'display': 'inline-block', "margin-left": "1%"}),
             dbc.Toast([html.P(f"{chi2}")], header="Chi2", style={'display': 'inline-block', "margin-left": "1%"}),
             dbc.Toast([html.P(f"{dof}")], header="Degrees of Freedom",
                       style={'display': 'inline-block', "margin-left": "1%"})])
        return df.to_json(orient="records"), toasts, dbc.Table.from_dataframe(df, striped=False, bordered=True,
                                                                              hover=True)
    return [], [], []


@app.callback(
    Output("download-output", "data"),
    [Input("download-button", "n_clicks"), Input("memory-output", "data"), Input("send-button", "n_clicks")],
    prevent_initial_call=True
)
def download_chi_squared(n_clicks, data, sent):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data and "download-button" in changed_id and sent:
        df = pd.read_json(data)
        return dcc.send_data_frame(df.to_csv, "mydf.csv")
