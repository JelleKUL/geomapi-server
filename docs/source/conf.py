# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import configparser
import datetime
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------
config = configparser.ConfigParser()
config.read("../../setup.cfg")
release = config["metadata"]["version"]
author = config["metadata"]["author"]
project = config["metadata"]["name"]
copyright = str(datetime.date.today().year) + ", " + author

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    #'myst_parser',
    'myst_nb'
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
autodoc_mock_imports = config["options"]["install_requires"].splitlines()

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
templates_path = ['_templates']
exclude_patterns = []
# Options for the notebook parsing
nb_execution_mode = "off"
# Options for Myst markdown parsing
myst_enable_extensions = ["dollarmath", "amsmath", "html_image"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

#Build instructions:
# cd ./docs 
# sphinx-quickstart 
# sphinx-apidoc -o . ..\segmentationtools\
# ./make html

# sphinx-apidoc -o ./docs/source/api .\api\ -e -t ./docs/source/_templates
# sphinx-build -b html docs/source/ docs/_build