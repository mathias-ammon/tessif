# tessif/frused/resolutions.py
"""Tessif's temporal and spatial resolution parameters.

:mod:`~tessif.frused.resolutions` is a :mod:`tessif` aggregating frequently
needed temporal resolution parameters.
"""

temporal_support = [
    "daily",
    "hourly",
    "30min",
    "15min",
    "10min",
    "5min",
    "min",
    "30s",
    "15s",
    "10s",
    "5s",
    "s",
]
"""
Supported temporal resolution aliases. Use
:attr:`~tessif.frused.resolutions.temporals` for accessing them.

.. csv-table:: Currently supported temporal resolution aliases
    :file: docs/source/csvs/resolutions/temporal_support.csv
"""


temporals = {i: i for i in temporal_support}
"""
Mapping temporal support tags to themself for failsafe resolution access.

.. csv-table:: first column labels the keys
    :file: docs/source/csvs/resolutions/temporals.csv
    :stub-columns: 1
"""

#: `Rounding Aliases
#: <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`_
#: for supported temporal resolutions.
temporal_rounding_map = {
    "daily": "D",
    "hourly": "H",
    "30min": "30min",
    "15min": "15min",
    "10min": "10min",
    "5min": "5min",
    "min": "min",
    "30s": "30S",
    "15s": "15S",
    "10s": "10S",
    "5s": "5S",
    "s": "S",
}
"""
`Rounding aliases
<https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`_
for supported temporal resolutions. Used when parsing in spreadsheet data.

.. csv-table:: first column labels the keys
    :file: docs/source/csvs/resolutions/temporal_rounding_map.csv
    :stub-columns: 1
"""
