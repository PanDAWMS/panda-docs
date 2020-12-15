# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'PanDAWMS'
copyright = '2020, PanDA'
author = 'PanDA'

import sphinx_rtd_theme

extensions = [
    "sphinx_rtd_theme",
    'sphinx-prompt',
    'nbsphinx',
]

nbsphinx_execute = 'never'

html_theme = "sphinx_rtd_theme"

templates_path = ['_templates']
exclude_patterns = []

html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html', 'searchbox.html'] }

html_show_sourcelink = False

html_logo = 'images/PanDA-rev-logo-small-200px.jpg'

html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'titles_only': True,
}

def setup (app):
    app.add_css_file('custom.css')