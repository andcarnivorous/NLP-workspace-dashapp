"""
This module creates the instance of the Home page.
"""

from utils import generate_app

app = generate_app(__name__, url_base_pathname='/text_classification/')
