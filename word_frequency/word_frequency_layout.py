import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from global_components.utils import make_info_toast, display_page
from word_frequency.word_frequency import app
from word_frequency.word_frequency_callbacks import make_box, \
    make_download_button_tab1, make_download_button_tab2, make_ngram_slider_tab1, concordance_limit_slider
from word_frequency.word_vector_tab import make_box_vector, \
    make_download_button_vector
from global_components.menu import navbar
from global_components.layout import Layout
from word_frequency import concordance_callbacks

jumbo = html.Div([
    dbc.Jumbotron([
        html.H1("Word Frequency Toolkit",
                className="display-3"),
        html.H2(
            "Get word frequency data, word vectors and graphs from your corpora.",
            className="lead",
        )])])

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Tokenize from File", tab_id="tab-1"),
                    dbc.Tab(label="Tokenize from Text", tab_id="tab-2"),
                    dbc.Tab(label="Concordance", tab_id="tab-concordance"),
                    dbc.Tab(label="Word Vectors", tab_id="tab-vector"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

tab_len = html.Div([
    dcc.Input(
        id="input_len",
        type="number",
        placeholder="10", debounce=True, max=100)])

download_button = html.Div(dbc.Button('Download', id='download-button', n_clicks=0, color="dark", className="mr-111"))

extra_stopwords = html.Div([html.H5("Extra stopwords:"),
                            dcc.Textarea(
                                id='extra-stopwords',
                                value='',
                                style={'height': 90}, )])

textarea = dcc.Textarea(
    id='textarea-example',
    value='Textarea contenot initialized\nwith multiple lines of text',
    style={'height': 300, "width": "100%"},
)

layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])

layout_instance = Layout(tabs=["Tokenize from File", "Tokenize from Text", "Concordance", "Word Vectors"],
                         preprocessing={"Remove Stopwords": "stopwords",
                                        "Remove Punctuation": "punct",
                                        "Apply Stemming": "stem"},
                         buttons={"confirmation": ["Send", "send-button"],
                                  "plotting": ["BarPlot", "plot-button"],
                                  "plotting-vector": ["Scatter Plot", "plot-button-vector"]})

base = html.Div([navbar, jumbo,
                 html.Div([layout_instance.tabs])])

toasts = layout_instance.make("token-stats-toasts", style={'display': 'inline-block'})


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-3":
        ret_value = html.Div([
            html.Center(html.Div(
                [dbc.ButtonGroup([layout_instance.buttons["confirmation"],
                                  layout_instance.buttons["plotting"],
                                  make_download_button_tab1()]),
                 make_box(), html.H5("word/pattern"),
                 dcc.Input(id="word", type="text", maxLength=300), concordance_limit_slider(), html.Hr(),
                 layout_instance.make("output-concordance-plot"), layout_instance.make("output-concordance"),  # toasts,
                 make_info_toast("How to Use",
                                 "Upload a text file and choose a word for concordance")]))])
        return ret_value

    if active_tab == "tab-2":
        ret_value = html.Div([
            html.Div([dbc.ButtonGroup([layout_instance.buttons["confirmation"],
                                       layout_instance.buttons["plotting"],
                                       make_download_button_tab2()])],
                     style={'width': '100%', 'display': 'inline-block'}),
            html.Div([
                html.Div([textarea, layout_instance.preprocessing, extra_stopwords, tab_len, make_ngram_slider_tab1()],
                         style={'width': '45%', 'display': 'inline-block'}),
                html.Div([], style={'width': '10%', 'display': 'inline-block'}),
                html.Hr(),
                html.Div(
                    [dcc.Loading(id='textarea-example-output'), toasts,
                     layout_instance.make("output-data-plot2", kind="load"), dcc.Store(id='memory')],
                    style={'width': '45%', 'display': 'inline-block'})], className="row")])
        return ret_value

    elif active_tab == "tab-4":
        return html.Div([make_info_toast("How to Use",
                                         "Upload a txt file, set the preprocessing you want,"
                                         "you can add custom stopwords, then push the SEND button."),
                         html.Center(make_box_vector()),
                         layout_instance.make("output-data-upload-vector"),
                         layout_instance.make("output-data-plot-vector"),
                         layout_instance.buttons["plotting-vector"], make_download_button_vector()])

    ret_val = html.Div([
        html.Center(html.Div(
            [dbc.ButtonGroup([layout_instance.buttons["confirmation"], layout_instance.buttons["plotting"],
                              make_download_button_tab1()]), make_box(), html.Hr()],
            style={'width': '100%', 'display': 'inline-block', "margin-bottom": "3%"})),
        html.Div([
            html.Div([layout_instance.preprocessing, extra_stopwords, tab_len, make_ngram_slider_tab1()],
                     style={'width': '45%', 'display': 'inline-block'}),
            html.Div([], style={'width': '5%', 'display': 'inline-block'}),
            html.Div([layout_instance.make("output-data-plot", kind="load"),
                      layout_instance.make("output-data-upload"),
                      toasts,
                      make_info_toast("How to Use",
                                      "Upload a txt file, set the preprocessing you want, you can add custom stopwords, then push the SEND button.")
                      ], style={'width': '45%', 'display': 'inline-block'}),
        ], className="row")
    ])

    return ret_val


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display(pathname):
    return display_page(pathname, "word_freq", base)
