# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'vng_api'
copyright = '2026, Lena During'
author = 'Lena During'
release = 'v1.150.2'
master_doc = 'index'
add_module_names = False

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'recommonmark',
    'sphinx_paramlinks',
    'sphinx_favicon',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.apidoc'
]

apidoc_modules = [
    {
        'path': '../../vng_api',
        'destination': 'reference',
        'module_first': True,
        'member_order': 'bysource',
        'automodule_options': ('members', 'undoc-members', 'show-inheritance')
    }
]
apidoc_module_dir = '../../vng_api'
apidoc_excluded_paths = ['tests', '.venv']
apidoc_separate_modules = True
apidoc_module_first = True
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'aio': ('https://docs.aiohttp.org/en/stable/', None)
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "pygments_dark_style": "monokai",
}
html_static_path = ['_static']
