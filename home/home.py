"""
This module creates the instance of the Home page.
"""

from utils import generate_app
import dash
import dash_bootstrap_components as dbc
from server.server import server

app = generate_app(__name__, url_base_pathname='/')
