"""Sphinx configuration."""
project = "Helium Api Wrapper"
author = "Lukas Huber"
copyright = "2022, Lukas Huber"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
