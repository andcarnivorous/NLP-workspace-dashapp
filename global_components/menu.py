import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Vowel Clustering", href="/vowel/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Word Frequency", href="/word_freq/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Chi-squared", href="/chi_squared/", external_link=True)),
        dbc.NavItem(dbc.NavLink("Text Classification", href="/text_classification/", external_link=True)),

        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Blog linguistica", href="https://bloglinguistica.press", external_link=True),
                dbc.DropdownMenuItem("About", href="/about", external_link=True),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Home",
    brand_href="/", brand_external_link=True,
)
