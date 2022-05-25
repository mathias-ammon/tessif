# docs/conf.py
"""Sphinx configuration."""
project = "tessif - Transforming Energy Supply System modell I ng Frameworks"
author = "Mathias Ammon"
copyright = f"2022, {author}"

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
    # 'style_nav_header_background': '#009682',
}

# Sort the documentation
autodoc_member_order = "bysource"
