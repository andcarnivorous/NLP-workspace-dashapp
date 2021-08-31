import io
import json
import logging
import os

import dash
import dash_bootstrap_components as dbc
import dash_table
import google.cloud.logging
import pandas as pd
import plotly.express as px

from server.server import server


def load_module_configs(path="configs/dash_modules.json"):
    with open(path) as config_file:
        modules = json.load(config_file)
    return modules


def generate_logger(name):
    on_cloud = os.getenv("K_SERVICE", None)

    handler = None
    if on_cloud:
        client = google.cloud.logging.Client()
        handler = client.get_default_handler()
        client.setup_logging()

    log_format = "[%(levelname)s] %(name)s:%(lineno)d : %(message)s"
    logging.basicConfig(format=log_format)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if on_cloud:
        logger.addHandler(handler)

    return logger


def generate_app(name, url_base_pathname):
    return dash.Dash(name, server=server, external_stylesheets=[dbc.themes.LUX],
                     url_base_pathname=f"{url_base_pathname}", title="NLP Workspace")


def df_to_barplot(df):
    # deprecated, use Plotter instance
    fig = px.bar(df, x="Token", y="Frequency")
    fig.update_layout(title={'text': "Bar Chart", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    return fig


def df_to_table(df: pd.DataFrame):
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns]
    )
    return table


def parse_file(decoded_payload: bytes, content_type: str, list_of_names: list) -> pd.DataFrame:
    """
    Decode and read the contents of incoming file into a pandas dataframe.

    :param decoded_payload: bytes incoming payload file, this should be a tabulated file
    :param content_type: str should contain the information necessary to infer file format
    :param list_of_names:
    :return:
    """
    df = None
    if 'csv' in content_type:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded_payload.decode('utf-8')))
    elif 'xls' in content_type or list_of_names and list_of_names[0].endswith("xls"):
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded_payload))
    elif 'xlsx' in content_type or list_of_names and list_of_names[0].endswith("xlsx"):
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded_payload), engine="openpyxl")
    elif "text" in content_type:
        df = pd.read_fwf(
            io.StringIO(decoded_payload.decode('utf-8')))
    return df


class GeneratorWrapper:
    def __init__(self, generator_function):
        self.generator_function = generator_function
        self.generator = self.generator_function()

    def __iter__(self):
        # reset the generator
        self.generator = self.generator_function()
        return self

    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result
