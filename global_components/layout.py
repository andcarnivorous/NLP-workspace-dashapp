import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

COMPONENTS = {"div": html.Div, "load": dcc.Loading}


class Layout:

    def __init__(self, tabs: list = [], preprocessing: dict = {}, buttons: dict = {}):
        self.tabs = tabs
        self.preprocessing = preprocessing
        self.buttons = buttons

    @property
    def tabs(self):
        return self._tabs

    @tabs.setter
    def tabs(self, value):
        self._tabs = dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label=f"{name}", tab_id=f"tab-{n}") for n, name in enumerate(value, start=1)
                        ],
                        id="card-tabs",
                        card=True,
                        active_tab="tab-1",
                    )
                ),
                dbc.CardBody(html.P(id="card-content", className="card-text")),
            ]
        )

    @property
    def preprocessing(self):
        return self._preprocessing

    @preprocessing.setter
    def preprocessing(self, value):
        self._preprocessing = dbc.FormGroup(
            [
                dbc.Label("Apply Preprocessing"),
                dbc.Checklist(
                    options=[
                        {"label": k, "value": v} for k, v in value.items()
                    ],
                    value=[],
                    id="switches-input",
                    switch=True, inline=True
                ),
            ]
        )

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, value):
        buttons_dict = {key: dbc.Button(val[0], id=val[1], n_clicks=0, color="dark") for key, val in value.items()}
        self._buttons = buttons_dict

    @staticmethod
    def make(name, kind="div", **kwargs):
        func = COMPONENTS[kind]
        return func(id=name, **kwargs)