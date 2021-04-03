import io

import pandas as pd


def parse_file(decoded_payload: bytes, content_type: str, list_of_names: list) -> pd.DataFrame:
    """
    Decode and read the contents of incoming file into a pandas dataframe.

    :param decoded_payload: bytes incoming payload file, this should be a tabulated file
    :param content_type: str should contain the information necessary to infer file format
    :param list_of_names:
    :return:
    """
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