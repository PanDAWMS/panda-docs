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
import os
import sys
import subprocess

from docutils import nodes
from sphinx import addnodes

sys.path.insert(0, os.path.abspath('.'))


# a role that renders a gdpconfig parameter name as inline code linking to the gdpconfig page.
# The literal wraps the xref (not vice versa) so the monospace node survives xref resolution,
# which otherwise rebuilds the inner node of an explicit doc reference.
def gdp_param_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    xref = addnodes.pending_xref(
        rawtext, nodes.Text(text),
        refdomain='std', reftype='doc',
        reftarget='/advanced/gdpconfig', refexplicit=True,
    )
    node = nodes.literal(rawtext, '', xref, classes=['gdp-param'])
    return [node], []


# -- Project information -----------------------------------------------------

project = 'PanDAWMS'
copyright = '2026, PanDA'
author = 'PanDA'

import sphinx_rtd_theme

extensions = [
    "sphinx_rtd_theme",
    'sphinx_prompt',
    'nbsphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx_tabs.tabs',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain'
]

sphinx_tabs_disable_tab_closing = True
sphinx_tabs_valid_builders = ['linkcheck']

nbsphinx_execute = 'never'
autosectionlabel_prefix_document = True
todo_include_todos = True

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

rst_prolog = """
.. |br| raw:: html

   <br />
   
.. role:: raw-html(raw)
    :format: html
    
.. role:: red

.. role:: blue

.. role:: orange

.. role:: hblue

.. role:: green

.. role:: purple

.. role:: brown
   
"""


def setup (app):
    app.add_role('gdp', gdp_param_role)
    app.add_css_file('custom.css')
    # adjust location of action file depending on build mechanism
    action_file = 'extra_actions.sh'
    src_dir = 'source'
    if not os.getcwd().endswith(src_dir):
        action_file = os.path.join(src_dir, action_file)
    else:
        src_dir = '.'
    # extra actions
    if os.path.exists(action_file):
        subprocess.run('/bin/bash {} {}'.format(action_file, src_dir), universal_newlines=True,
                       shell=True, stdout=sys.stdout, stderr=sys.stderr)

