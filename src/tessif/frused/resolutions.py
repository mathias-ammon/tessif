# tessif/frused/resolutions.py
# -*- coding: utf-8 -*-
"""
:mod:`~tessif.frused.resolutions` is a :mod:`tessif` aggregating frequently
needed temporal resolution parameters.
"""

temporal_support = [
    'daily', 'hourly',
    '30min', '15min', '10min', '5min', 'min',
    '30s', '15s', '10s', '5s', 's']
"""
Supported temporal resolution aliases. Use
:attr:`~tessif.frused.resolutions.temporals` for accessing them.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.resolutions import temporal_support
    import pandas
    import tessif.frused.spellings as sps


    path = os.path.join(
         doc_dir, 'source', 'api', 'frused',
        'resolutions', 'temporal_support.csv')

    sps.to_csv(temporal_support, 'temporal_support', path=path)


.. csv-table:: Currently supported temporal resolution aliases
    :file: source/api/frused/resolutions/temporal_support.csv
"""


temporals = {i: i for i in temporal_support}
"""
Mapping temporal support tags to themself for failsafe resolution access.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.resolutions import temporals
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'resolutions', 'temporals.csv')

    df = pandas.DataFrame(data=temporals.values(),
                          index=temporals.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the keys
    :file: source/api/frused/resolutions/temporals.csv
    :stub-columns: 1
"""

#: `Rounding Aliases
#: <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`_
#: for supported temporal resolutions.
temporal_rounding_map = {
    'daily': 'D',
    'hourly': 'H',
    '30min': '30min',
    '15min': '15min',
    '10min': '10min',
    '5min': '5min',
    'min': 'min',
    '30s': '30S',
    '15s': '15S',
    '10s': '10S',
    '5s': '5S',
    's': 'S',
}
"""
`Rounding aliases
<https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`_
for supported temporal resolutions. Used when parsing in spreadsheet data.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.resolutions import temporal_rounding_map
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'resolutions', 'temporal_rounding_map.csv')

    df = pandas.DataFrame(data=temporal_rounding_map.values(),
                          index=temporal_rounding_map.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the keys
    :file: source/api/frused/resolutions/temporal_rounding_map.csv
    :stub-columns: 1
"""
