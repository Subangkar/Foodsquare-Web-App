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
sys.path.insert(0, os.path.abspath('..'))
# from django.conf import settings
# settings.configure()
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Foodsquare.settings'
django.setup()

# -- Project information -----------------------------------------------------

project = 'Foodsquare'
copyright = '2019, Subangkar Karmaker, Masum Rahman, Mohaimin Saquib'
author = 'Subangkar Karmaker, Masum Rahman, Mohaimin Saquib'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# html_theme = 'alabaster'

import sphinx_glpi_theme
html_theme = "glpi"
html_theme_path = sphinx_glpi_theme.get_html_themes_path()


# import edx_theme

# extensions = ['edx_theme']

# copyright = '{year}, edX Inc.'.format(year=datetime.datetime.now().year)
# author = edx_theme.AUTHOR

# html_theme = 'edx_theme'
# html_theme_path = [edx_theme.get_html_theme_path()]
# html_favicon = os.path.join(html_theme_path[0], 'edx_theme', 'static', 'css', 'favicon.ico')

# latex_documents = [
#     (master_doc, 'edx-sphinx-theme.tex', 'edx-sphinx-theme Documentation',
#      author, 'manual'),
# ]


# import rtcat_sphinx_theme
# html_theme = "rtcat_sphinx_theme"
# html_theme_path = [rtcat_sphinx_theme.get_html_theme_path()]


# import sphinx_rtd_theme
# html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]