# tessif/transform/mapping2es/tsf/__init__.py
"""
:mod:`~tessif.transform.mapping2es.tsf` is a :mod:`tessif` package to transform
abstract energy system data represented as `mapping
<https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_ into
ready to simulate energy system model instances.

Mapping like representations are usually returned by utilities part of the
:mod:`~tessif.parse` module.
"""
from tessif.write import log
import pandas as pd
from tessif.frused import resolutions, spellings, configurations
from tessif.frused.defaults import energy_system_nodes as esn
from tessif.model import components, energy_system
import tessif.namedtuples as nts


def _generate_busses(energy_system_dict):
    """
    Generate :class:`~tessif.model.components.Bus` objects
    out of the :paramref:`~generate_busses.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionary of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_busses: ~collections.abc.Generator
        Generator object yielding the parsed
        :class:`bus objects <tessif.model.components.Bus>`.

    """
    busses = spellings.get_from(energy_system_dict, smth_like='bus',
                                dflt=pd.DataFrame())

    for row, bus in busses.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed
        if spellings.get_from(bus, smth_like='active', dflt=esn['active']):

            yield components.Bus(
                name=spellings.get_from(
                    bus, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    bus, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    bus, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    bus, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    bus, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    bus, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    bus, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    bus, smth_like='node_type',
                    dflt=esn['node_type']),
                inputs=spellings.get_from(
                    bus, smth_like='input',
                    dflt=esn['input']),
                outputs=spellings.get_from(
                    bus, smth_like='output',
                    dflt=esn['output']),)


[docs]
@log.timings
def _generate_sinks(energy_system_dict):
    """
    Generate :class:`~tessif.model.components.Sink` objects
    out of the :paramref:`~generate_sinks.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_sinks: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`sink objects <tessif.model.components.Sink>`.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Using the pure_python energy system mapping example

    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> sinks = ttsf._generate_sinks(parse.python_mapping(m))
    """
    sinks = spellings.get_from(energy_system_dict, smth_like='sink',
                               dflt=pd.DataFrame())

    for row, sink in sinks.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed
        if spellings.get_from(sink, smth_like='active', dflt=esn['active']):

            # parse inputs beforehand to set adequate defaults
            inputs = *spellings.get_from(
                sink, smth_like='inputs', dflt=esn['input']),

            yield components.Sink(
                name=spellings.get_from(
                    sink, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    sink, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    sink, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    sink, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    sink, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    sink, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    sink, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    sink, smth_like='node_type',
                    dflt=esn['node_type']),
                inputs=inputs,

                # linear problem parameters
                accumulated_amounts=spellings.get_from(
                    sink, smth_like='accumulated_amounts',
                    dflt={k: nts.MinMax(
                        min=esn['minimum'], max=esn['maximum'])
                        for k in inputs}),

                flow_rates=spellings.get_from(
                    sink, smth_like='flow_rates',
                    dflt={k: nts.MinMax(
                        esn['minimum'], esn['maximum']) for k in inputs}),

                flow_costs=spellings.get_from(
                    sink, smth_like='flow_costs',
                    dflt={k: esn['flow_costs'] for k in inputs}),

                flow_emissions=spellings.get_from(
                    sink, smth_like='flow_emissions',
                    dflt={k: esn['emissions'] for k in inputs}),

                flow_gradients=spellings.get_from(
                    sink, smth_like='flow_gradients',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient'], esn['negative_gradient'])
                        for k in inputs}),

                gradient_costs=spellings.get_from(
                    sink, smth_like='gradient_costs',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient_costs'],
                        esn['negative_gradient_costs'])
                        for k in inputs}),

                timeseries=spellings.get_from(
                    sink, smth_like='timeseries',
                    dflt=esn['timeseries']),

                # expansion problem parameters
                expandable=spellings.get_from(
                    sink, smth_like='expandable',
                    dflt={k: esn['expandable'] for k in inputs}),

                expansion_costs=spellings.get_from(
                    sink, smth_like='expansion_costs',
                    dflt={k: esn['expansion_costs'] for k in inputs}),

                expansion_limits=spellings.get_from(
                    sink, smth_like='expansion_limits',
                    dflt={k: nts.MinMax(
                        esn['minimum_expansion'],
                        esn['maximum_expansion']) for k in inputs}),

                # mixed integer linear problem
                milp=spellings.get_from(
                    sink, smth_like='milp',
                    dflt={k: esn['milp'] for k in inputs}),

                initial_status=spellings.get_from(
                    sink, smth_like='initial_status',
                    dflt=esn['initial_status']),

                status_inertia=spellings.get_from(
                    sink, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['minimum_uptime'],
                        esn['minimum_downtime'])),

                status_changing_costs=spellings.get_from(
                    sink, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['startup_costs'],
                        esn['shutdown_costs'])),

                number_of_status_changes=spellings.get_from(
                    sink, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['maximum_shutdowns'],
                        esn['maximum_startups'])),

                costs_for_being_active=spellings.get_from(
                    sink, smth_like='costs_for_being_active',
                    dflt=esn['costs_for_being_active']),
            )


[docs]
@log.timings
def _generate_sources(energy_system_dict):
    """
    Generate :class:`~tessif.model.components.Source`
    objects out of the :paramref:`~generate_sources.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_sources: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`source<tessif.model.components.Source>`
        objects.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Using the pure_python energy system mapping example

    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> sources = ttsf._generate_sources(parse.python_mapping(m)
    """
    sources = spellings.get_from(energy_system_dict, smth_like='source',
                                 dflt=pd.DataFrame())

    for row, source in sources.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed
        if spellings.get_from(source, smth_like='active', dflt=esn['active']):

            # parse outputs beforehand to set adequate defaults
            outputs = *spellings.get_from(
                source, smth_like='outputs', dflt=esn['output']),

            yield components.Source(
                name=spellings.get_from(
                    source, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    source, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    source, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    source, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    source, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    source, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    source, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    source, smth_like='node_type',
                    dflt=esn['node_type']),
                outputs=outputs,

                # linear problem parameters
                accumulated_amounts=spellings.get_from(
                    source, smth_like='accumulated_amounts',
                    dflt={k: nts.MinMax(
                        min=esn['minimum'], max=esn['maximum'])
                        for k in outputs}),

                flow_rates=spellings.get_from(
                    source, smth_like='flow_rates',
                    dflt={k: nts.MinMax(
                        esn['minimum'], esn['maximum']) for k in outputs}),

                flow_costs=spellings.get_from(
                    source, smth_like='flow_costs',
                    dflt={k: esn['flow_costs'] for k in outputs}),

                flow_emissions=spellings.get_from(
                    source, smth_like='flow_emissions',
                    dflt={k: esn['emissions'] for k in outputs}),

                flow_gradients=spellings.get_from(
                    source, smth_like='flow_gradients',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient'], esn['negative_gradient'])
                        for k in outputs}),

                gradient_costs=spellings.get_from(
                    source, smth_like='gradient_costs',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient_costs'],
                        esn['negative_gradient_costs'])
                        for k in outputs}),

                timeseries=spellings.get_from(
                    source, smth_like='timeseries',
                    dflt=esn['timeseries']),

                # expansion problem parameters
                expandable=spellings.get_from(
                    source, smth_like='expandable',
                    dflt={k: esn['expandable'] for k in outputs}),

                expansion_costs=spellings.get_from(
                    source, smth_like='expansion_costs',
                    dflt={k: esn['expansion_costs'] for k in outputs}),

                expansion_limits=spellings.get_from(
                    source, smth_like='expansion_limits',
                    dflt={k: nts.MinMax(
                        esn['minimum_expansion'],
                        esn['maximum_expansion']) for k in outputs}),

                # mixed integer linear problem
                milp=spellings.get_from(
                    source, smth_like='milp',
                    dflt={k: esn['milp'] for k in outputs}),

                initial_status=spellings.get_from(
                    source, smth_like='initial_status',
                    dflt=esn['initial_status']),

                status_inertia=spellings.get_from(
                    source, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['minimum_uptime'],
                        esn['minimum_downtime'])),

                status_changing_costs=spellings.get_from(
                    source, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['startup_costs'],
                        esn['shutdown_costs'])),

                number_of_status_changes=spellings.get_from(
                    source, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['maximum_shutdowns'],
                        esn['maximum_startups'])),

                costs_for_being_active=spellings.get_from(
                    source, smth_like='costs_for_being_active',
                    dflt=esn['costs_for_being_active']),
            )


[docs]
@log.timings
def _generate_transformers(energy_system_dict):
    r"""
    Generate :class:`~tessif.model.components.Transformer`
    objects out of the :paramref:`~generate_transformers.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_transformers: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`transformer<tessif.model.components.Transformer>`
        objects.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Using the pure_python energy system mapping example

    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> transformers = ttsf._generate_transformers(parse.python_mapping(m))
    """
    transformers = spellings.get_from(
        energy_system_dict, smth_like='transformer',
        dflt=pd.DataFrame())

    for row, transformer in transformers.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed

        if spellings.get_from(
                transformer, smth_like='active', dflt=esn['active']):

            # parse inputs beforehand to set adequate defaults
            inputs = *spellings.get_from(
                transformer, smth_like='inputs', dflt=esn['input']),

            # parse outputs beforehand to set adequate defaults
            outputs = *spellings.get_from(
                transformer, smth_like='outputs', dflt=esn['output']),

            yield components.Transformer(
                name=spellings.get_from(
                    transformer, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    transformer, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    transformer, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    transformer, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    transformer, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    transformer, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    transformer, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    transformer, smth_like='node_type',
                    dflt=esn['node_type']),

                inputs=inputs,
                outputs=outputs,
                conversions=spellings.get_from(
                    transformer, smth_like='efficiency',
                    dflt=esn['efficiency']),

                # linear problem parameters
                flow_rates=spellings.get_from(
                    transformer, smth_like='flow_rates',
                    dflt={k: nts.MinMax(
                        esn['minimum'], esn['maximum'])
                        for k in [*inputs, *outputs]}),

                flow_costs=spellings.get_from(
                    transformer, smth_like='flow_costs',
                    dflt={k: esn['flow_costs'] for k in [*inputs, *outputs]}),

                flow_emissions=spellings.get_from(
                    transformer, smth_like='flow_emissions',
                    dflt={k: esn['emissions'] for k in [*inputs, *outputs]}),

                flow_gradients=spellings.get_from(
                    transformer, smth_like='flow_gradients',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient'], esn['negative_gradient'])
                        for k in [*inputs, *outputs]}),

                gradient_costs=spellings.get_from(
                    transformer, smth_like='gradient_costs',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient_costs'],
                        esn['negative_gradient_costs'])
                        for k in [*inputs, *outputs]}),

                timeseries=spellings.get_from(
                    transformer, smth_like='timeseries',
                    dflt=esn['timeseries']),

                # expansion problem parameters
                expandable=spellings.get_from(
                    transformer, smth_like='expandable',
                    dflt={k: esn['expandable'] for k in [*inputs, *outputs]}),

                expansion_costs=spellings.get_from(
                    transformer, smth_like='expansion_costs',
                    dflt={k: esn['expansion_costs']
                          for k in [*inputs, *outputs]}),

                expansion_limits=spellings.get_from(
                    transformer, smth_like='expansion_limits',
                    dflt={k: nts.MinMax(
                        esn['minimum_expansion'],
                        esn['maximum_expansion'])
                        for k in [*inputs, *outputs]}),

                # mixed integer linear problem
                milp=spellings.get_from(
                    transformer, smth_like='milp',
                    dflt={k: esn['milp']
                          for k in [*inputs, *outputs]}),

                initial_status=spellings.get_from(
                    transformer, smth_like='initial_status',
                    dflt=esn['initial_status']),

                status_inertia=spellings.get_from(
                    transformer, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['minimum_uptime'],
                        esn['minimum_downtime'])),

                status_changing_costs=spellings.get_from(
                    transformer, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['startup_costs'],
                        esn['shutdown_costs'])),

                number_of_status_changes=spellings.get_from(
                    transformer, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['maximum_shutdowns'],
                        esn['maximum_startups'])),

                costs_for_being_active=spellings.get_from(
                    transformer, smth_like='costs_for_being_active',
                    dflt=esn['costs_for_being_active']),
            )


def _generate_chps(energy_system_dict):
    r"""
    Generate :class:`~tessif.model.components.CHP` objects out of the
    :paramref:`~generate_chps.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_chps: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`chp <tessif.model.components.CHP>`
        objects.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Store the create_variable_chp example from the hardcoded examples into a
    hdf5 file and then parse it into a mapping from which the chps are
    generated.

    >>> import tessif.examples.data.tsf.py_hard as tsf_examples
    >>> tsf_es = tsf_examples.create_variable_chp()
    >>> import os
    >>> from tessif.frused.paths import write_dir
    >>> output_msg = tsf_es.to_hdf5(
    ...     directory=os.path.join(write_dir, 'tsf'),
    ...     filename='chp_es.hdf5',
    ... )
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> chps = ttsf._generate_chps(parse.hdf5(
    ...     path=os.path.join(write_dir, 'tsf', 'chp_es.hdf5'),))
    >>> for c in chps:
    ...     for name, atr in c.attributes.items():
    ...         print('{}: {}'.format(
    ...             name, sorted(atr) if isinstance(atr, frozenset) else atr))
    ... # frozensets are printed as sorted lists for doctesting consistency
    back_pressure: nan
    conversion_factor_full_condensation: {('gas', 'electricity'): 0.5}
    conversions: {('gas', 'electricity'): 0.3, ('gas', 'heat'): 0.2}
    costs_for_being_active: 0.0
    el_efficiency_wo_dist_heat: MinMax(min=nan, max=nan)
    enthalpy_loss: MinMax(min=nan, max=nan)
    expandable: {'electricity': False, 'gas': False, 'heat': False}
    expansion_costs: {'electricity': 0.0, 'gas': 0.0, 'heat': 0.0}
    expansion_limits: {'electricity': MinMax(min=0.0, max=inf), 'gas': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0.0, max=inf)}
    flow_costs: {'electricity': 3, 'gas': 0, 'heat': 2}
    flow_emissions: {'electricity': 2, 'gas': 0, 'heat': 3}
    flow_gradients: {'electricity': PositiveNegative(positive=inf, negative=inf), 'gas': PositiveNegative(positive=inf, negative=inf), 'heat': PositiveNegative(positive=inf, negative=inf)}
    flow_rates: {'electricity': MinMax(min=0, max=9), 'gas': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0, max=6)}
    gradient_costs: {'electricity': PositiveNegative(positive=0.0, negative=0.0), 'gas': PositiveNegative(positive=0.0, negative=0.0), 'heat': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status: 1
    inputs: ['gas']
    interfaces: ['electricity', 'gas', 'heat']
    milp: {'electricity': False, 'gas': False, 'heat': False}
    min_condenser_load: nan
    number_of_status_changes: OnOff(on=0, off=0)
    outputs: ['electricity', 'heat']
    power_loss_index: nan
    power_wo_dist_heat: MinMax(min=nan, max=nan)
    status_changing_costs: OnOff(on=0, off=0)
    status_inertia: OnOff(on=0, off=0)
    timeseries: None
    uid: CHP1
    back_pressure: False
    conversion_factor_full_condensation: {}
    conversions: {}
    costs_for_being_active: 0.0
    el_efficiency_wo_dist_heat: MinMax(min=[0.43, 0.43, 0.43, 0.43], max=[0.53, 0.53, 0.53, 0.53])
    enthalpy_loss: MinMax(min=[1.0, 1.0, 1.0, 1.0], max=[0.18, 0.18, 0.18, 0.18])
    expandable: {'electricity': False, 'gas': False, 'heat': False}
    expansion_costs: {'electricity': 0.0, 'gas': 0.0, 'heat': 0.0}
    expansion_limits: {'electricity': MinMax(min=0.0, max=inf), 'gas': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0.0, max=inf)}
    flow_costs: {'electricity': 3, 'gas': 0, 'heat': 2}
    flow_emissions: {'electricity': 2, 'gas': 0, 'heat': 3}
    flow_gradients: {'electricity': PositiveNegative(positive=inf, negative=inf), 'gas': PositiveNegative(positive=inf, negative=inf), 'heat': PositiveNegative(positive=inf, negative=inf)}
    flow_rates: {'electricity': MinMax(min=0.0, max=inf), 'gas': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0.0, max=inf)}
    gradient_costs: {'electricity': PositiveNegative(positive=0.0, negative=0.0), 'gas': PositiveNegative(positive=0.0, negative=0.0), 'heat': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status: 1
    inputs: ['gas']
    interfaces: ['electricity', 'gas', 'heat']
    milp: {'electricity': False, 'gas': False, 'heat': False}
    min_condenser_load: [3, 3, 3, 3]
    number_of_status_changes: OnOff(on=0, off=0)
    outputs: ['electricity', 'heat']
    power_loss_index: [0.19, 0.19, 0.19, 0.19]
    power_wo_dist_heat: MinMax(min=[8, 8, 8, 8], max=[20, 20, 20, 20])
    status_changing_costs: OnOff(on=0, off=0)
    status_inertia: OnOff(on=0, off=0)
    timeseries: None
    uid: CHP2
    """
    chps = spellings.get_from(
        energy_system_dict, smth_like='combined_heat_power',
        dflt=pd.DataFrame())

    for row, chp in chps.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed

        if spellings.get_from(
                chp, smth_like='active', dflt=esn['active']):
            # parse inputs beforehand to set adequate defaults
            inputs = *spellings.get_from(
                chp, smth_like='inputs', dflt=esn['input']),

            # parse outputs beforehand to set adequate defaults
            outputs = *spellings.get_from(
                chp, smth_like='outputs', dflt=esn['output']),

            yield components.CHP(
                name=spellings.get_from(
                    chp, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    chp, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    chp, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    chp, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    chp, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    chp, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    chp, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    chp, smth_like='node_type',
                    dflt=esn['node_type']),

                inputs=inputs,
                outputs=outputs,
                back_pressure=spellings.get_from(
                    chp, smth_like='back_pressure',
                    dflt=esn['chp_back_pressure']),

                conversion_factor_full_condensation=spellings.get_from(
                    chp, smth_like='conversion_factor_full_condensation',
                    dflt=esn['chp_efficiency']),

                el_efficiency_wo_dist_heat=spellings.get_from(
                    chp, smth_like='el_efficiency_wo_dist_heat',
                    dflt=esn['el_efficiency_wo_dist_heat']),

                enthalpy_loss=spellings.get_from(
                    chp, smth_like='enthalpy_loss',
                    dflt=esn['enthalpy_loss']),

                min_condenser_load=spellings.get_from(
                    chp, smth_like='min_condenser_load',
                    dflt=esn['min_condenser_load']),

                power_loss_index=spellings.get_from(
                    chp, smth_like='power_loss_index',
                    dflt=esn['power_loss_index']),

                power_wo_dist_heat=spellings.get_from(
                    chp, smth_like='power_wo_dist_heat',
                    dflt=esn['power_wo_dist_heat']),

                conversions=spellings.get_from(
                    chp, smth_like='efficiency',
                    dflt=esn['chp_efficiency']),

                # linear problem parameters
                flow_rates=spellings.get_from(
                    chp, smth_like='flow_rates',
                    dflt={k: nts.MinMax(
                        esn['minimum'], esn['maximum'])
                        for k in [*inputs, *outputs]}),

                flow_costs=spellings.get_from(
                    chp, smth_like='flow_costs',
                    dflt={k: esn['flow_costs'] for k in [*inputs, *outputs]}),

                flow_emissions=spellings.get_from(
                    chp, smth_like='flow_emissions',
                    dflt={k: esn['emissions'] for k in [*inputs, *outputs]}),

                flow_gradients=spellings.get_from(
                    chp, smth_like='flow_gradients',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient'], esn['negative_gradient'])
                        for k in [*inputs, *outputs]}),

                gradient_costs=spellings.get_from(
                    chp, smth_like='gradient_costs',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient_costs'],
                        esn['negative_gradient_costs'])
                        for k in [*inputs, *outputs]}),

                timeseries=spellings.get_from(
                    chp, smth_like='timeseries',
                    dflt=esn['timeseries']),

                # expansion problem parameters
                expandable=spellings.get_from(
                    chp, smth_like='expandable',
                    dflt={k: esn['expandable'] for k in [*inputs, *outputs]}),

                expansion_costs=spellings.get_from(
                    chp, smth_like='expansion_costs',
                    dflt={k: esn['expansion_costs']
                          for k in [*inputs, *outputs]}),

                expansion_limits=spellings.get_from(
                    chp, smth_like='expansion_limits',
                    dflt={k: nts.MinMax(
                        esn['minimum_expansion'],
                        esn['maximum_expansion'])
                        for k in [*inputs, *outputs]}),

                # mixed integer linear problem
                milp=spellings.get_from(
                    chp, smth_like='milp',
                    dflt={k: esn['milp']
                          for k in [*inputs, *outputs]}),

                initial_status=spellings.get_from(
                    chp, smth_like='initial_status',
                    dflt=esn['initial_status']),

                status_inertia=spellings.get_from(
                    chp, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['minimum_uptime'],
                        esn['minimum_downtime'])),

                status_changing_costs=spellings.get_from(
                    chp, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['startup_costs'],
                        esn['shutdown_costs'])),

                number_of_status_changes=spellings.get_from(
                    chp, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['maximum_shutdowns'],
                        esn['maximum_startups'])),

                costs_for_being_active=spellings.get_from(
                    chp, smth_like='costs_for_being_active',
                    dflt=esn['costs_for_being_active']),
            )


[docs]
@log.timings
def _generate_storages(energy_system_dict):
    """
    Generate :class:`~tessif.model.components.Storage`
    objects out of the :paramref:`~generate_storages.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_storages: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`storage<tessif.model.components.Storage>`
        objects.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Using the pure_python energy system mapping example

    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> storages = ttsf._generate_storages(parse.python_mapping(m))
    >>> for s in storages:
    ...     print(s.uid)
    ...     print(s.input)
    ...     print(s.output)
    ...     for name, atr in s.attributes.items():
    ...         print('{}: {}'.format(
    ...             name, sorted(atr) if isinstance(atr, frozenset) else atr))
    ...     # frozensets are printed as sorted lists for doctesting consistency
    Battery
    electricity
    electricity
    capacity: 100
    costs_for_being_active: 0
    expandable: {'electricity': False}
    expansion_costs: {'electricity': 0}
    expansion_limits: {'electricity': MinMax(min=0, max=inf)}
    final_soc: None
    fixed_expansion_ratios: {'electricity': True}
    flow_costs: {'electricity': 0}
    flow_efficiencies: {'electricity': InOut(inflow=0.95, outflow=0.98)}
    flow_emissions: {'electricity': 0}
    flow_gradients: {'electricity': PositiveNegative(positive=10, negative=10)}
    flow_rates: {'electricity': MinMax(min=0, max=10)}
    gradient_costs: {'electricity': PositiveNegative(positive=0, negative=0)}
    idle_changes: PositiveNegative(positive=0, negative=1)
    initial_soc: 10
    initial_status: True
    input: electricity
    interfaces: ['electricity']
    milp: {'electricity': False}
    number_of_status_changes: OnOff(on=0, off=2)
    output: electricity
    status_changing_costs: OnOff(on=0, off=2)
    status_inertia: OnOff(on=0, off=2)
    timeseries: None
    uid: Battery
    """
    storages = spellings.get_from(
        energy_system_dict, smth_like='generic_storage',
        dflt=pd.DataFrame())

    for row, storage in storages.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed

        if spellings.get_from(
                storage, smth_like='active', dflt=esn['active']):

            # parse inputs beforehand to set adequate defaults
            input = spellings.get_from(
                storage, smth_like='input', dflt=esn['input'])

            # parse outputs beforehand to set adequate defaults
            output = spellings.get_from(
                storage, smth_like='output', dflt=esn['output'])

            storage = components.Storage(
                name=spellings.get_from(
                    storage, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    storage, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    storage, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    storage, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    storage, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    storage, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    storage, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    storage, smth_like='node_type',
                    dflt=esn['node_type']),

                input=input,
                output=output,

                capacity=spellings.get_from(
                    storage, smth_like='storage_capacity',
                    dflt=esn['storage_capacity']),

                initial_soc=spellings.get_from(
                    storage, smth_like='initial_soc',
                    dflt=esn['initial_soc']),

                idle_changes=spellings.get_from(
                    storage, smth_like='idle_changes',
                    dflt=nts.PositiveNegative(
                        esn['gain_rate'], esn['loss_rate'])),

                flow_rates=spellings.get_from(
                    storage, smth_like='flow_rates',
                    dflt={k: nts.MinMax(
                        esn['minimum'], esn['maximum'])
                        for k in [input, output]}),

                flow_costs=spellings.get_from(
                    storage, smth_like='flow_costs',
                    dflt={k: esn['flow_costs'] for k in [input, output]}),

                flow_efficiencies=spellings.get_from(
                    storage, smth_like='flow_efficiencies',
                    dflt={k: nts.InOut(
                        inflow=esn['efficiency'], outflow=esn['efficiency'])
                        for k in [input, output]},
                ),

                flow_emissions=spellings.get_from(
                    storage, smth_like='flow_emissions',
                    dflt={k: esn['emissions'] for k in [input, output]}),

                flow_gradients=spellings.get_from(
                    storage, smth_like='flow_gradients',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient'], esn['negative_gradient'])
                        for k in [input, output]}),

                gradient_costs=spellings.get_from(
                    storage, smth_like='gradient_costs',
                    dflt={k: nts.PositiveNegative(
                        esn['positive_gradient_costs'],
                        esn['negative_gradient_costs'])
                        for k in [input, output]}),

                timeseries=spellings.get_from(
                    storage, smth_like='timeseries',
                    dflt=esn['timeseries']),

                # expansion problem parameters
                expandable=spellings.get_from(
                    storage, smth_like='expandable',
                    dflt={k: esn['expandable']
                          for k in [input, output, 'capacity']}),

                fixed_expansion_ratios=spellings.get_from(
                    storage, smth_like='fixed_expansion_ratios',
                    dflt={k: esn['fixed_expansion_ratios']
                          for k in [input, output]}),

                expansion_costs=spellings.get_from(
                    storage, smth_like='expansion_costs',
                    dflt={k: esn['expansion_costs']
                          for k in [input, output, 'capacity']}),

                expansion_limits=spellings.get_from(
                    storage, smth_like='expansion_limits',
                    dflt={k: nts.MinMax(
                        esn['minimum_expansion'],
                        esn['maximum_expansion'])
                        for k in [input, output, 'capacity']}),

                # mixed integer linear problem
                milp=spellings.get_from(
                    storage, smth_like='milp',
                    dflt={k: esn['milp']
                          for k in [input, output]}),

                initial_status=spellings.get_from(
                    storage, smth_like='initial_status',
                    dflt=esn['initial_status']),

                status_inertia=spellings.get_from(
                    storage, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['minimum_uptime'],
                        esn['minimum_downtime'])),

                status_changing_costs=spellings.get_from(
                    storage, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['startup_costs'],
                        esn['shutdown_costs'])),

                number_of_status_changes=spellings.get_from(
                    storage, smth_like='status_inertia',
                    dflt=nts.OnOff(
                        esn['maximum_shutdowns'],
                        esn['maximum_startups'])),

                costs_for_being_active=spellings.get_from(
                    storage, smth_like='costs_for_being_active',
                    dflt=esn['costs_for_being_active']),
            )

            yield storage


[docs]
@log.timings
def _generate_connectors(energy_system_dict):
    r"""
    Generate :class:`~tessif.model.components.Connector`
    objects out of the :paramref:`~generate_transformers.energy_system_dict`.

    Parameters
    ----------
    energy_system_dict: dict
        Dictionairy of :class:`pandas.DataFrame` objects keyed by strings.
        With the key strings representing energy system components.
        Usually returned by something like the :mod:`tessif.parse`
        functionalities.

    Return
    ------
    generated_connectors: ~collections.abc.Generator
        Generator obeject yielding the parsed
        :class:`connector <tessif.model.components.Connector>`
        objects.

    Examples
    --------
    Setting :attr:`spellings.get_from's <tessif.frused.spellings.get_from>`
    logging level to debug for decluttering doctest output:

    >>> from tessif.frused import configurations
    >>> configurations.spellings_logging_level = 'debug'

    Using the pure_python energy system mapping example

    >>> import tessif.examples.data.tsf.py_mapping.transshipment as tship
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> connectors = ttsf._generate_connectors(
    ...     parse.python_mapping(tship.mapping))
    >>> for c in connectors:
    ...     for name, atr in c.attributes.items():
    ...         print('{}: {}'.format(
    ...             name, sorted(atr) if isinstance(atr, frozenset) else atr))
    ... # frozensets are printed as sorted lists for doctesting consistency
    conversions: {('bus-01', 'bus-02'): 0.9, ('bus-02', 'bus-01'): 0.8}
    inputs: ['bus-01', 'bus-02']
    interfaces: ['bus-01', 'bus-02']
    outputs: ['bus-01', 'bus-02']
    timeseries: None
    uid: connector
    """
    connectors = spellings.get_from(
        energy_system_dict, smth_like='connector',
        dflt=pd.DataFrame())

    for row, connector in connectors.iterrows():
        # check active switch, but assume user forgot adding one
        # and meant to add all entries listed

        if spellings.get_from(
                connector, smth_like='active', dflt=esn['active']):

            # parse interface beforehand to set adequate defaults
            # a connectors interface is both it's inputs as well it's outputs
            interfaces = *spellings.get_from(
                connector, smth_like='interfaces', dflt=esn['interfaces']),

            yield components.Connector(
                name=spellings.get_from(
                    connector, smth_like='name',
                    dflt=esn['name']),
                latitude=spellings.get_from(
                    connector, smth_like='latitude',
                    dflt=esn['latitude']),
                longitude=spellings.get_from(
                    connector, smth_like='longitude',
                    dflt=esn['longitude']),
                region=spellings.get_from(
                    connector, smth_like='region',
                    dflt=esn['region']),
                sector=spellings.get_from(
                    connector, smth_like='sector',
                    dflt=esn['sector']),
                carrier=spellings.get_from(
                    connector, smth_like='carrier',
                    dflt=esn['carrier']),
                component=spellings.get_from(
                    connector, smth_like='component',
                    dflt=esn['component']),
                node_type=spellings.get_from(
                    connector, smth_like='node_type',
                    dflt=esn['node_type']),

                interfaces=interfaces,

                conversions=spellings.get_from(
                    connector, smth_like='efficiency',
                    dflt=esn['efficiency']),

                # # expansion problem parameters
                # expandable=spellings.get_from(
                #     connector, smth_like='expandable',
                #     dflt={k: esn['expandable'] for k in [*inputs, *outputs]}),

                # expansion_costs=spellings.get_from(
                #     connector, smth_like='expansion_costs',
                #     dflt={k: esn['expansion_costs']
                #           for k in [*inputs, *outputs]}),

                # expansion_limits=spellings.get_from(
                #     connector, smth_like='expansion_limits',
                #     dflt={k: nts.MinMax(
                #         esn['minimum_expansion'],
                #         esn['maximum_expansion'])
                #         for k in [*inputs, *outputs]}),

            )


[docs]
@log.timings
def infer_timeindex(energy_system_dict):
    """
    Try inferring the timeindex from the energy system dictionary.
    Inferring is done by reading out the
    :attr:`~tessif.frused.spellings.timeindex`-like column
    of the :attr:`~tessif.frused.spellings.timeseries`-like spreadsheet
    (:class:`~pandas.DataFrame`) and rounding it according to the
    :attr:`temporal resolution
    <tessif.frused.configurations.temporal_resolution>`.

    The timeframe to be simulated is here referred to as "timeindex".

    Warning
    -------
    For inferring to be succesfull, discrete timeframe length has to be at
    least 3 (after rounding).

    Parameters
    ----------
    energy_system_dict: dict
        Dictionary containing the energy system data. Typically returned by
        one of the :mod:`tessif.parse` functionalities

    Return
    ------
    timeindex: pandas.DatetimeIndex
        The time frame inferred from the energy system dictionary.

    Example
    -------
    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> from tessif.frused.paths import example_dir
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> idx = ttsf.infer_timeindex(parse.python_mapping(m))
    >>> import pprint
    >>> pprint.pprint(idx)
    DatetimeIndex(['1990-07-13 00:00:00', '1990-07-13 01:00:00',
                   '1990-07-13 02:00:00'],
                  dtype='datetime64[ns]', freq='H')
    """

    # find out which expression of 'Timeframe' was used
    ts_key = [variant for variant in spellings.timeframe
              if variant in energy_system_dict.keys()][0]

    # find out which expression of 'Timeindex' was used
    idx_key = [variant for variant in spellings.timeindex
               if variant in energy_system_dict[ts_key].columns][0]

    # logger.debug(
    #    ("Inferring timeframe using '{}' for timeframe and "
    #     "'{}' for timeindex".format(
    #        ts_key, idx_key))

    # Extract the time index
    timeindex = pd.DatetimeIndex(
        energy_system_dict[ts_key][idx_key].values, freq='infer')

    # Round to time index according to temporal resolution settings to...
    # correct rounding errors of the input source due to time format display
    timeindex = timeindex.round(
        resolutions.temporal_rounding_map[configurations.temporal_resolution])

    # Reinfer frequency from newly round time index
    timeindex = pd.DatetimeIndex(timeindex, freq='infer')

    # If reinferring was unsuccessful, enforce tessif's current frequency
    if timeindex.freq is None:
        timeindex.freq = resolutions.temporal_rounding_map[
            configurations.temporal_resolution]

    return timeindex


[docs]
@log.timings
def transform(energy_system_mapping, **kwargs):
    """
    Transform an :meth:`energy system mapping
    <tessif.parse.python_mapping>` to a :class:`tessif energy system
    <tessif.model.energy_system>`.

    Parameters
    ----------
    energy_system_mapping: dict
        Dictionairy containing the energy system data. Typically returned by
        one of the :mod:`tessif.parse` functionalities

    timeframe: pandas.DatetimeIndex
        Datetime index representing the evaluated timeframe. Explicitly
        stating:

            - initial datatime
              (0th element of the :class:`pandas.DatetimeIndex`)
            - number of timesteps (length of :class:`pandas.DatetimeIndex`)
            - temporal resolution (:attr:`pandas.DatetimeIndex.freq`)

        For example::

            idx = pd.DatetimeIndex(
                data=pd.date_range(
                    '2016-01-01 00:00:00', periods=11, freq='H'))

        Note
        ----
        If not stated it is tried to be :meth:`inferred<infer_timeindex>`.

    global_constraints: dict, default={'emissions': float('+inf')}
        Dictionairy of :class:`numeric <numbers.Number>` values mapped to
        global constraint naming :class:`strings <str>`.

        Recognized constraint keys are:

            - ``emissions``
            - ...

        For a more detailed explanation see the user guide's section:
        :ref:`Secondary_Objectives`

    uid: ~collections.abc.Hashable, default='automatically_transformed'
        Hashable unique identifier. Usually a string aka a name.

    Return
    ------
    energy_system: ~tessif.model.energy_system.AbstractEnergySystem
        The dictionairy transformed oemof energy system, ready for simulation.

    Examples
    --------
    Using the pure_python energy system mapping example:

    >>> from tessif.examples.data.tsf.py_mapping.fpwe import mapping as m
    >>> import tessif.parse as parse
    >>> import tessif.transform.mapping2es.tsf as ttsf
    >>> esys = ttsf.transform(parse.python_mapping(m))
    >>> for node in esys.nodes:
    ...     for k, v in node.attributes.items():
    ...         print('{} = {}'.format(
    ...             k, sorted(v) if isinstance(v, frozenset) else v))
    ... # frozensets are printed as sorted lists for doctesting consistency
    ...     print(50*'-')
    ...     print()
    inputs = ['Gas Station.fuel']
    interfaces = ['Gas Station.fuel', 'Generator.fuel']
    outputs = ['Generator.fuel']
    timeseries = None
    uid = Pipeline
    --------------------------------------------------
    <BLANKLINE>
    inputs = ['Battery.electricity', 'Generator.electricity']
    interfaces = ['Battery.electricity', 'Demand.electricity', 'Generator.electricity']
    outputs = ['Battery.electricity', 'Demand.electricity']
    timeseries = None
    uid = Power Line
    --------------------------------------------------
    <BLANKLINE>
    accumulated_amounts = {'fuel': MinMax(min=0, max=inf)}
    costs_for_being_active = 0
    expandable = {'fuel': False}
    expansion_costs = {'fuel': 0}
    expansion_limits = {'fuel': MinMax(min=0, max=inf)}
    flow_costs = {'fuel': 0}
    flow_emissions = {'fuel': 0}
    flow_gradients = {'fuel': PositiveNegative(positive=42, negative=42)}
    flow_rates = {'fuel': MinMax(min=0, max=22)}
    gradient_costs = {'fuel': PositiveNegative(positive=1, negative=1)}
    initial_status = True
    interfaces = ['fuel']
    milp = {'fuel': False}
    number_of_status_changes = OnOff(on=1, off=1)
    outputs = ['fuel']
    status_changing_costs = OnOff(on=1, off=1)
    status_inertia = OnOff(on=1, off=1)
    timeseries = {'fuel': MinMax(min=0, max=array([10, 22, 22]))}
    uid = Gas Station
    --------------------------------------------------
    <BLANKLINE>
    accumulated_amounts = {'electricity': MinMax(min=0, max=inf)}
    costs_for_being_active = 0
    expandable = {'electricity': False}
    expansion_costs = {'electricity': 0}
    expansion_limits = {'electricity': MinMax(min=0, max=inf)}
    flow_costs = {'electricity': 0}
    flow_emissions = {'electricity': 0}
    flow_gradients = {'electricity': PositiveNegative(positive=11, negative=11)}
    flow_rates = {'electricity': MinMax(min=8, max=11)}
    gradient_costs = {'electricity': PositiveNegative(positive=0, negative=0)}
    initial_status = True
    inputs = ['electricity']
    interfaces = ['electricity']
    milp = {'electricity': False}
    number_of_status_changes = OnOff(on=2, off=1)
    status_changing_costs = OnOff(on=2, off=1)
    status_inertia = OnOff(on=2, off=1)
    timeseries = None
    uid = Demand
    --------------------------------------------------
    <BLANKLINE>
    conversions = {('fuel', 'electricity'): 0.42}
    costs_for_being_active = 0
    expandable = {'electricity': False, 'fuel': False}
    expansion_costs = {'electricity': 0, 'fuel': 0}
    expansion_limits = {'electricity': MinMax(min=0, max=inf), 'fuel': MinMax(min=0, max=inf)}
    flow_costs = {'electricity': 0, 'fuel': 0}
    flow_emissions = {'electricity': 0, 'fuel': 0}
    flow_gradients = {'electricity': PositiveNegative(positive=10, negative=10), 'fuel': PositiveNegative(positive=50, negative=50)}
    flow_rates = {'electricity': MinMax(min=5, max=15), 'fuel': MinMax(min=0, max=50)}
    gradient_costs = {'electricity': PositiveNegative(positive=0, negative=0), 'fuel': PositiveNegative(positive=0, negative=0)}
    initial_status = True
    inputs = ['fuel']
    interfaces = ['electricity', 'fuel']
    milp = {'electricity': True, 'fuel': False}
    number_of_status_changes = OnOff(on=0, off=2)
    outputs = ['electricity']
    status_changing_costs = OnOff(on=0, off=2)
    status_inertia = OnOff(on=0, off=2)
    timeseries = {'electricity': MinMax(min=0, max=array([10, 22, 22]))}
    uid = Generator
    --------------------------------------------------
    <BLANKLINE>
    capacity = 100
    costs_for_being_active = 0
    expandable = {'electricity': False}
    expansion_costs = {'electricity': 0}
    expansion_limits = {'electricity': MinMax(min=0, max=inf)}
    final_soc = None
    fixed_expansion_ratios = {'electricity': True}
    flow_costs = {'electricity': 0}
    flow_efficiencies = {'electricity': InOut(inflow=0.95, outflow=0.98)}
    flow_emissions = {'electricity': 0}
    flow_gradients = {'electricity': PositiveNegative(positive=10, negative=10)}
    flow_rates = {'electricity': MinMax(min=0, max=10)}
    gradient_costs = {'electricity': PositiveNegative(positive=0, negative=0)}
    idle_changes = PositiveNegative(positive=0, negative=1)
    initial_soc = 10
    initial_status = True
    input = electricity
    interfaces = ['electricity']
    milp = {'electricity': False}
    number_of_status_changes = OnOff(on=0, off=2)
    output = electricity
    status_changing_costs = OnOff(on=0, off=2)
    status_inertia = OnOff(on=0, off=2)
    timeseries = None
    uid = Battery
    --------------------------------------------------
    <BLANKLINE>

    Get the inspected timeframe:

    >>> print(esys.timeframe)
    DatetimeIndex(['1990-07-13 00:00:00', '1990-07-13 01:00:00',
                   '1990-07-13 02:00:00'],
                  dtype='datetime64[ns]', freq='H')

    Use the automatically generated energy system to :meth:`transform
    <tessif.model.energy_system.Abstract EnergySystem.to_nxgrph>` it into a
    :class:`networkx.Graph` to facilitate plotting:

    >>> import tessif.visualize.nxgrph as nxv
    >>> import matplotlib.pyplot as plt
    >>> grph = esys.to_nxgrph()
    >>> drawings = nxv.draw_graph(
    ...     grph, node_color='green', edge_color='pink')
    >>> plt.draw()

    IGNORE:
    >>> title = plt.gca().set_title(
    ...     'transform.tsf module design example')
    >>> plt.pause(2)
    >>> plt.close('all')

    IGNORE

    .. image:: transformed_es_example.png
        :align: center
        :alt: alternate text
    """

    # get/default global constraints
    global_constraints = kwargs.pop(
        'global_constraints',
        energy_system_mapping.get(
            'global_constraints',
            {'emissions': float('+inf')}))

    # get/infer timeindex
    timeindex = kwargs.pop(
        'timeframe', infer_timeindex(energy_system_mapping))

    # get/autofill uid
    _uid = kwargs.pop(
        'uid', 'automatically_transformed')

    busses = _generate_busses(energy_system_mapping)
    sinks = _generate_sinks(energy_system_mapping)
    sources = _generate_sources(energy_system_mapping)
    transformers = _generate_transformers(energy_system_mapping)
    chps = _generate_chps(energy_system_mapping)
    storages = _generate_storages(energy_system_mapping)
    connectors = _generate_connectors(energy_system_mapping)

    # Create energy system object
    es = energy_system.AbstractEnergySystem(
        uid=_uid,
        busses=busses,
        connectors=connectors,
        sinks=sinks,
        sources=sources,
        transformers=transformers,
        chps=chps,
        storages=storages,
        timeframe=timeindex,
        global_constraints=global_constraints)

    return es
