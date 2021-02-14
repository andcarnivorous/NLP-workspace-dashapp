import base64
import io
import pandas as pd
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from modeller import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

models = [{"label": "KMeans", "value": "KMeans"}, {"label": "AgglomerativeClustering", "value": "AgglomerativeClustering"}, {"label": "DBSCAN", "value": "DBSCAN"}]

params = {"KMeans": {"n_clusters": 5, "n_init": 1, "max_iter": 550}, "AgglomerativeClustering": {"n_clusters": 5}, "DBSCAN": {"eps": 0.18, "min_samples": 3}}
all_params = {"n_init": 1, "max_iter": 550, "n_clusters": 5, "eps": 0.18, "min_samples": 3}
limits = {"n_init": 50, "max_iter": 550, "n_clusters": 50, "eps": 0.9, "min_samples": 55}

inputs = [Input(f"input_{k}", "value") for k in all_params] + [Input("column1", "value"), Input("column2", "value")]

columns = [{"label":"F1", "value":"F1"}, {"label":"F2", "value":"F2"},{"label":"F3", "value":"F3"}, {"label":"F4", "value":"F4"}]

app.layout = html.Div([

    html.Div([
    dbc.Jumbotron(
    [
        html.H1("Unsupervised Clustering of Vowels", className="display-3"),
        html.P(
            "Insert your vowel's dataset and perform clustering",
            className="lead",
        )])]),
    html.Div([
        dcc.RadioItems(id="column1",
                       options=columns,
                       value='F1',
                       labelStyle={'display': 'inline-block'})]),
    html.Div([
        dcc.RadioItems(id="column2",
                       options=columns,
                       value='F2',
                       labelStyle={'display': 'inline-block'})]),

            html.Div([
        dcc.RadioItems(id="model-type",
            options=models,
            value='DBSCAN',
            labelStyle={'display': 'inline-block'}),
    html.Div(id='output-params')]),
    dcc.Upload(
        id='upload-data', max_size=5e+7,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Hr(),
    html.Div(dcc.Loading(id="output-data-upload")),
    html.Div(id='output-data-table')])


@app.callback(Output('output-params', 'children'),
              Input('model-type', 'value'))
def update_params(model_type):
        if model_type:
            parameters = all_params
            htmlparams = html.Div(
                [
                    dcc.Input(
                        id=f"input_{k}",
                        type="number",
                        placeholder=f"{k}:{v}", max=limits[k],
                        readOnly=True if k not in params[model_type] else False,
                        style={"color":"red" if k not in params[model_type] else "green"}
                    )
                    for k,v in parameters.items()
                ]
            )
            return htmlparams


@app.callback(Output('upload-data', 'children'),
              [Input('upload-data', 'contents')] + [State('upload-data', 'filename'), State('upload-data', 'last_modified')])
def upload_box(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        contents = list_of_contents[0]
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        return html.P(f"{list_of_names[0]}")
    else:
        return html.Div(['Drag and Drop or ', html.A('Select Files')])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'), Input("model-type", "value")] + inputs +
              [State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def update_output(list_of_contents, model_type, n_init, max_iter, n_clusters, eps, min_samples, column1, column2, list_of_names, list_of_dates):
    if list_of_contents is not None:
        if column1 == column2:
            return html.P("Select different columns!")

        contents = list_of_contents[0]
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in content_type:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in content_type:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
            elif "text" in content_type:
                df = pd.read_fwf(
                    io.StringIO(decoded.decode('utf-8')))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        if len(df.columns) > 8:
            return html.P("Dataframe has too many columns!")
        model = Modeller(df, model_type, **dict(n_init=n_init, max_iter=max_iter, n_clusters=n_clusters, eps=eps, min_samples=min_samples))
        try:
            labels = model.set_up_model([column1, column2])
        except Exception as e:
            return html.P(str(e))
        if not labels:
            return html.P("Please, fill in all the parameters in green.")
        return dcc.Graph(id="chart", figure=labels, style={'display': 'block',
                                                           'height': 600,
                                                           'width': 900,
                                                            'margin-left': 'auto',
                                                            'margin-right': 'auto'})
    return html.P("")


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
