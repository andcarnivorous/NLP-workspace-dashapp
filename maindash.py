"""
from home.home import app as home
from home.home_layout import layout as home_layout
from server.server import server
from vowel_clustering.vowel_clustering import app as vwl_clst
from vowel_clustering.vowel_clustering_layout import layout as vwl_clast_layout
from word_frequency.word_frequency import app as wf
from word_frequency.word_frequency_layout import base as wf_layout
from chi_squared.chi_squared import app as chi_squared_app
from chi_squared.chi_squared_layout import base as chi_squared_layout_var
from global_components.utils import layout
from text_classification.text_classification import app as text_classification_app
from text_classification.text_classification_layout import base as text_classification_layout

app = home
app.layout = layout  # home_layout

app1 = vwl_clst
app1.layout = layout  # vwl_clst_layout

app2 = wf
app2.layout = layout  # layout  # wf_layout

app3 = chi_squared_app
app3.layout = layout  # chi_squared_layout_var

app4 = text_classification_app
app4.layout = layout
"""
import os
from importlib import import_module

from global_components.module_generator import ModuleGenerator
from server.server import server
from utils import load_module_configs

apps = []
modules = load_module_configs()
existing_modules = [f.path[2:] for f in os.scandir() if f.is_dir() and f.path[2:] in modules]

for module, endpoint in modules.items():
    if module not in existing_modules:
        module_generator = ModuleGenerator(".", module)
        module_generator.generate_new_module()
    dash_app = getattr(import_module(f"{module}.{module}"), "app")
    dash_app.layout = getattr(import_module(f"{module}.{module}_layout"), "layout")
    apps.append(dash_app)

if __name__ == "__main__":
    server.run(debug=False, host="0.0.0.0", port=8080)
