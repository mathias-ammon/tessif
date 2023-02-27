# tessif/frused/configurations.py
"""Package-wide configurations.

:mod:`~tessif.frused.configurations` is a :mod:`tessif` subpackage aggregating
frequently used parameters, used naming and unit conventions as well as some
logging behavior.

It serves as main reference point for adjusting Tessif's parsing behavior.
"""


temporal_resolution = "hourly"
"""
Currently used temporal resolution. Must be one of the keys found in
:attr:`~tessif.frused.resolutions.temporals`.

Currently set to::

    from tessif.frused.configurations import temporal_resolution
    print(temporal_resolution)
    hourly
"""

node_uid_style = "name"
"""
Switch for tweaking internal node uid representation style.

Useful for conveniently changing internal mapping behaviour. Must be one of
:attr:`~tessif.frused.namedtuples.node_uid_styles`.

Somehting like ``name`` allows for quick and intuitive node accessing while
sacrificing the possibility of 2 nodes having the same
:paramref:`~tessif.frused.namedtuples.Uid.name`.

``qualname`` on the other hand maps everything to the fully qualified name.
Meaning only ever the full combination of all
:class:`~tessif.frused.namedtuples.Uid` attributes has to be unique per
energy system.

.. warning::

    Tessif's doctests assumes ``node_uid_style = 'name'`` which is the most
    basic and intuitive way of mapping nodes. Designed for the use of
    relatively small energy systems (what ever that means).

For a list of available styles and their key (the string set to
:attr:`node_uid_style`) see :attr:`tessif.frused.namedtuples.node_uid_styles`.

Currently set to::

    from tessif.frused.configurations import node_uid_style
    print(node_uid_style)
    name
"""

node_uid_seperator = "_"
"""
Seperate different tags of the same
:attr:`node uid <tessif.frused.namedtuples.uid>`

Seperate symbol for (uniquely) identifying a node's uid using various tags of
the :attr:`namedtuples implementation <tessif.frused.namedtuples.Uid>`.

Currently set to::

    from tessif.frused.configurations import node_uid_seperator
    print(node_uid_seperator)
    _
"""

timeseries_seperator = "."
"""
Seperate energy system object and timeseries value.

Serperator symbol for identifying energy system object and its timeseries
values when reading in data.

Standard syntax::

    {ES_OBJECT}{SEPERATOR}{TIMESERIES_PARAMETER}.

Currently set to::

    import tessif.frused.configurations as config
    print(config.timeseries_seperator)
    .

So ``PV{SEPERATOR}max`` and ``Onshore{SEPERATOR}fix`` results in::

    import tessif.frused.configurations as config
    print(f"PV{config.timeseries_seperator}max")
    PV.max

    print(f"Onshore{config.timeseries_seperator}fix")
    Onshore.fix
"""

mimos = 10
"""
Number of seperate inputs/outputs supported for multiple input output energy
system transformers.

Currently set to::

        import tessif.frused.configurations as config
        print(config.mimos)
        10
"""

power_reference_unit = "MW"
"""
Unit to display power results with.

Currently set to::

        import tessif.frused.configurations as config
        print(config.power_reference_unit)
        MW
"""

cost_unit = "€"
"""
Unit representing the costs.

Currently set to::

        import tessif.frused.configurations as config
        print(config.cost_unit)
        €
"""

spellings_logging_level = "debug"
"""
`logging level
<https://docs.python.org/3/library/logging.html#logging-levels>`_
used by :meth:`spellings.get_from <tessif.frused.spellings.get_from>`.

Must be one of the keys found in :attr:`~tessif.write.log.logging_levels`.

Currently set to::

        import tessif.frused.configurations as config
        print(config.spellings_logging_level)
        info
"""

general_logging_level = "info"
"""
`logging level
<https://docs.python.org/3/library/logging.html#logging-levels>`_
used by :mod:`tessif.logging`.

Currently set to::

        import tessif.frused.configurations as config
        print(config.spellings_logging_level)
        info
"""

maximum_logging_file_size = 1 * 1024 * 2014
"""Maximum logging file size in bytes.

Currently set to::

        import tessif.frused.configurations as config
        print(config.maximum_logging_file_size)
        1048576  # 1 MB.
"""


maximum_number_of_logs = 13
"""Maximum number of kept logging files.

Currently set to::

        import tessif.frused.configurations as config
        print(config.maximum_number_of_logs)
        10
"""
