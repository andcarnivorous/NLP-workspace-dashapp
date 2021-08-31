import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from models.concordance_model import ConcordanceList
from word_frequency.word_frequency import app
import plotly.figure_factory as ff

@app.callback(
    [Output("output-concordance", "children"), Output("output-concordance-plot", "children")],
    [Input('memory1', 'data'),
     Input("send-button", "n_clicks"),
     Input("card-tabs", "active_tab"),
     Input("word", "value"),
     Input("slider-concordance", "value")],
    prevent_initial_call=True,
)
def update_file_processing(text, n_clicks, active_tab, word, limit):
    if active_tab == "tab-3":
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if "send-button" in changed_id or "slider-concordance" in changed_id:
            if text:
                concordance_list = ConcordanceList(text[0], word, limit)
                df = pd.DataFrame(concordance_list.rows)
                df.columns = ["prev", "word", "next"]
                table = dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_current=0,
                    page_size=100,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    style_data_conditional=[{"if": {"column_id": "word"}, "color": "red"}])

                words = np.array(concordance_list.records)
                matches_array = [np.where(words == word, 1, 0)]
                #iterator = (x for x in df.apply(lambda x: " ".join(x.values), axis=1).to_list())
                #def parse_iterator(i):
                #    try:
                #        return next(iterator)
                #    except StopIteration:
                #        return None
                #test = [parse_iterator(i) if i == 1 else '' for i in matches_array[0]]
                fig = go.Figure(data=go.Heatmap(z=matches_array,
                                                colorscale="gray", reversescale=True, showlegend=False, showscale=False))
                fig.update_layout(dict(xaxis=dict(showline=True, linewidth=1., linecolor='black', mirror=True),
                                       yaxis=dict(showline=True, showticklabels=False, linewidth=1., linecolor='black', mirror=True)),
                                  title='Concordance Plot')
                return [table, [dcc.Graph(id="concordance-heatmap", figure=fig)]]
            return [[], []]
        return [[], []]
    return [[], []]
