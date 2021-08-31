import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from vowel_clustering.configs import params, limits, all_params
import base64
from models.unsupervised_models import UnsupervisedModel
from utils import parse_file
from vowel_clustering.vowel_clustering import app
import dash

inputs = [Input(f"input_{k}", "value") for k in all_params] + \
         [Input("column1", "value"), Input("column2", "value")]


def confirmation_button():
    confirm_button = html.Div(dbc.Button('Send', id='send-button', n_clicks=0, color="dark", className="mr-1"))
    return confirm_button


def make_update():
    return dcc.Loading(id="output-data-upload")


def make_params():
    return html.Div(id='output-params')


def make_box():
    upload_box = dcc.Upload(
        id='upload-data', max_size=5e+6,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
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
        multiple=False
    )
    return upload_box


@app.callback(Output('output-data-upload', 'children'),
              [Input("send-button", "n_clicks"), Input('upload-data', 'contents'),
               Input("model-type", "value")] + inputs +
              [State('upload-data', 'filename'), State('upload-data', 'last_modified')])
def update_output(send_button, list_of_contents, model_type, n_init, max_iter, n_clusters, eps, min_samples, column1,
                  column2, list_of_names, list_of_dates):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "send-button" in changed_id:
        if list_of_contents:
            if column1 == column2:
                return html.P("Select different columns!")

            contents = list_of_contents
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                df = parse_file(decoded, content_type, list_of_names)
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])

            if len(df.columns) > 8:
                return html.P("Dataframe has too many columns!")

            model = UnsupervisedModel(df, model_type, **dict(n_init=n_init, max_iter=max_iter,
                                                             n_clusters=n_clusters, eps=eps,
                                                             min_samples=min_samples))
            try:
                labels = model.set_up_model([column1, column2])
            except Exception as e:
                return html.P(str(e))

            if not labels:
                return html.P("Please, fill in all the parameters in green.")
            return dcc.Graph(id="chart", figure=labels,
                             style={'display': 'block',
                                    'height': 600,
                                    'width': 900,
                                    'margin-left': 'auto',
                                    'margin-right': 'auto'})
        return dbc.Alert("You haven't uploaded files yet!", color="danger")


@app.callback(Output('output-params', 'children'),
              Input('model-type', 'value'))
def update_params(model_type):
    if model_type:
        parameters = all_params
        _inputs = [dbc.Input(
            id=f"input_{k}",
            type="number",
            placeholder=f"{k}:{v}", max=limits[k],
            disabled=True if k not in params[model_type] else False,
            style={
                "color": "white" if k not in params[model_type] else "black",
                "background-color": "white" if k not in params[model_type] else "",
                "border-width": "1px" if k in params[model_type] else "0px"}
        )
            for k, v in parameters.items()
        ]
        _prepends = [dbc.InputGroupAddon(f"{k}:", addon_type="prepend",
                                         style={"color": "white" if k not in params[model_type] else "grey",
                                                "border-pippo": "white" if k not in params[model_type] else "",
                                                "border-width": "1px" if k in params[model_type] else "0px",
                                                "border-style": "outset"})
                     for k in parameters.keys()]
        _parameters = []
        [_parameters.extend([_input, _prepend]) for _input, _prepend in zip(_prepends, _inputs)]
        htmlparams = dbc.InputGroup(_parameters)
        return htmlparams
    return


@app.callback(Output('upload-data', 'children'),
              [Input('upload-data', 'contents')] +
              [State('upload-data', 'filename'), State('upload-data', 'last_modified')])
def upload_box(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        contents = list_of_contents
        content_type, content_string = contents.split(',')
        return html.P(f"{list_of_names}")
    else:
        return html.Div(['Drag and Drop or ', html.A('Select Files')])
