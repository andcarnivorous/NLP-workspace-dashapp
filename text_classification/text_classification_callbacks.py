import dash
import dash_html_components as html
import requests
from dash.dependencies import Input, Output
import os
from text_classification.text_classification import app
from global_components.utils import make_output_toast
from utils import generate_logger

URL = os.getenv("TEXT_CLASSIFICATION_URL", "http://localhost:8000/classify/mlp/article/")

logger = generate_logger(__name__)


@app.callback(
    Output("classification-output", "children"),
    [Input('textarea-example', 'value'), Input("send-button", "n_clicks")],
    prevent_initial_call=True,
)
def update_output(text, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "send-button" in changed_id:
        response = requests.post(URL, json={"content": text, "id": "string", "category": "string"})
        if response.code >= 400:
            logger.error(f"Response returned {response.code}: {response.content}")
        return make_output_toast("Category", response.json()["result"])
