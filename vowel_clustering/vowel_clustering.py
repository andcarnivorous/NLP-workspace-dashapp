"""
This module creates the instance of the vowel_clustering dashboard.
"""
from utils import generate_app

app = generate_app(__name__, url_base_pathname='/vowel/')
