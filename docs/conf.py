# docs/conf.py
# pylint: disable=invalid-name
"""Sphinx configuration."""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import pathlib
import sys

# Make src and unittest folders knows to sphinx, to allow rtd to build the docs
src_path = pathlib.Path(__file__).resolve() / ".." / ".." / "src"
unittest_path = pathlib.Path(__file__).resolve() / ".." / ".."


sys.path.insert(0, os.path.abspath(unittest_path))
sys.path.insert(0, os.path.abspath(src_path))

# -- Project information -----------------------------------------------------

project = "tessif - Transforming Energy Supply System modell I ng Frameworks"
author = "Mathias Ammon"
copyright = f"2022, {author}"  # pylint: disable=redefined-builtin

extensions = [
    "sphinx.ext.autodoc",  # enable docstring documentation
    "sphinx.ext.autosummary",  # create linked tables for documented attributes
    "sphinx.ext.intersphinx",  # allow :mod: references to interlinked docs
    "sphinx.ext.napoleon",  # enable numpy style docstring syntax
    "sphinx.ext.viewcode",  # enable source links
    # 3rd party extensions
    # 'sphinx_execute_code',  # execute code
    "sphinx_paramlinks",  # enable :param: cross referencing
    # 'sphinxcontrib.excel_table',  # show xlsx exceltables
    # 'sphinxcontrib.exceltable',  # show xls exceltables
]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "canonical_url": "https://github.com/tZ3ma/tessif/",
    "display_version": True,
    "sticky_navigation": True,
}

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "matplotlib": ("https://matplotlib.org", None),
}

# Sort the documentation
autodoc_member_order = "bysource"


# pylint: enable=invalid-name
