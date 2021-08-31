import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils import generate_logger

logger = generate_logger(__name__)


class Plotter:

    def __init__(self, df: pd.DataFrame, col_1: str, col_2: str, kind: str = "bar", col_3: str = None, color=None,
                 **kwargs):
        self.df = df
        self.col_1 = col_1
        self.col_2 = col_2
        self.col_3 = col_3
        self.kind = kind
        self.color = color
        self.kwargs = kwargs

    def plot(self):
        plotting_func = getattr(self, self.kind)
        return plotting_func(self.df, self.col_1, self.col_2, self.col_3, self.color, **self.kwargs)

    def scatter(self, *args, **kwargs):
        if not self.col_3:
            fig = px.scatter(self.df, x=self.col_1, y=self.col_2, color=self.color)
            return fig

    def scatter_with_labels(self, *args, **kwargs):
        title = kwargs["title"]
        fig = go.Figure(
            data=go.Scatter(x=self.df[self.col_1], y=self.df[self.col_2], text=self.df.labels, mode="markers"))
        fig.update_layout(title={'text': title, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    def bar(self, *args, **kwargs):
        title = kwargs["title"]
        fig = px.bar(self.df, x=self.col_1, y=self.col_2)
        fig.update_layout(title={'text': title, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
        return fig
