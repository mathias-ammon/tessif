# tessif.frused.defaults
"""
:mod:`~tessif.frused.defaults` is a :mod:`tessif` subpackage providing
frequently needed defaults. Everything loosely associated with fallback
values as well as filter and sorting templates is aggregated here.
"""
import tessif.frused.namedtuples as nts
# from matplotlib import pyplot as plt
import tessif.frused.spellings as spellings

nxgrph_node_shapes = {
    'bus': 'o',
    'connector': 'o',
    'commodity_source': 'o',
    'default_source': 'o',
    'sink': '8',
    'solar': 's',
    'storage': 's',
    'transformer': '8',
    'wind': 'h',
}
"""
:mod:`~tessif.visualize.nxgrph` node shape visualization defaults.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nxgrph_node_shapes
    import dutils

    df = dutils.to_dataframe(nxgrph_node_shapes, columns=2, fillvalue='')

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'node_shapes.csv')

    df.to_csv(path, header=None, index=None, na_rep='None')

.. csv-table::
    :file: source/api/frused/defaults/node_shapes.csv
"""

dcgrph_node_shapes = {
    'default_source': 'round-rectangle',
    'commodity_source': 'round-rectangle',
    'solar': 'round-diamond',
    'wind': 'diamond',
    'bus': 'ellipse',
    'transformer': 'round-octagon',
    'connector': 'rectangle',

    'sink': 'ellipse',
    'storage': 'round-hexagon',
}
""":mod:`~tessif.visualize.dcgrph` node shape visualization defaults."""

nxgrph_visualize_defaults = {
    # node_defaults:
    'node_labels': None,
    'node_shape': 'o',
    'node_size': 3000,
    'node_minimum_size': 0.1 * 3000,
    'node_variable_size_scaling': 0.5,
    'node_fill_size': 3000,
    'node_color': '#AFAFAF',
    'node_color_map': ['#AFAFAF'],
    'node_alpha': 1.0,
    'node_font_size': 11,
    'node_font_weight': 'light',
    # edge defaults:
    'edge_labels': None,
    'edge_width': 1,
    'edge_color': 'black',
    'edge_arrowstyle': 'simple',
    'edge_arrowsize': 7,
    'edge_vmin': 0.0,
    'edge_vmax': 1.0,
    'edge_cmap': None,  # plt.cm.Greys,
    'edge_len': 1.0,
    'edge_minimum_grey': 0.15,
    'edge_minimum_weight': 0.1,
    'edge_minimum_width': 0.1,
    # legend defaults:
    'legend_labelspacing': 1,
    'legend_title': None,
    'legend_bbox_to_anchor': (1.0, 1),
    'legend_loc': 'best',
    'legend_borderaxespad': 0,
}
"""
:mod:`~tessif.visualize.nxgrph` drawing defaults.

Used as described in :func:`~tessif.visualize.nxgrph.draw_graph`'s
:paramref:`~tessif.visualize.nxgrph.draw_graph.kwargs`.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nxgrph_visualize_defaults
    import dutils

    nxgrph_visualize_defaults['edge_cmap'] = '.'.join(
        ['matplotlib.pyplot.cm', nxgrph_visualize_defaults['edge_cmap'].name])

    df = dutils.to_dataframe(
             nxgrph_visualize_defaults, columns=2, fillvalue='')

    path = os.path.join(
         doc_dir, 'source', 'api', 'frused',
        'defaults', 'nxgrph_visualize_defaults.csv')
    df.to_csv(path, header=None, index=None, na_rep='None')

.. csv-table::
    :file: source/api/frused/defaults/nxgrph_visualize_defaults.csv
"""

dcgrph_visualize_defaults = {
    # node_defaults:
    'node_labels': None,
    'node_label_position': 'center',
    'node_shape': "ellipse",
    'node_size': 90,
    # 'node_size_basic': 100,
    'node_color': '#AFAFAF',
    'node_font_size': 15,
    'node_minimum_size': 1,
    'node_variable_size': 40,
    'node_border_width': 0,
    'node_fill_border_width': 1.5,  # used when partially filling a node
    'node_border_style': None,  # 'solid',
    'node_border_color': "black",
    'node_font_weight': 550,
    # edge defaults:
    'edge_labels': None,
    'edge_width': 7,
    'edge_width_basic': 1,
    'edge_color': 'black',
    'edge_arrow_color': 'black',
    'edge_arrowsize': 1,
    'edge_arrowstyle': 'triangle',
    'edge_style': 'bezier',
    'edge_linestyle': 'solid',
    # replacing dotted by larger spaced dashes
    'edge_dot_repl_pattern': [6, 6],
    'edge_minimum_width': 0.5,
    'edge_minimum_grey': 0.15,
    'edge_minimum_weight': nxgrph_visualize_defaults['edge_minimum_weight'],
}
""":mod:`~tessif.visualize.dcgrph` drawing defaults.

Used as described in :func:`~tessif.visualize.dcgrph.draw_graph`'s
:paramref:`~tessif.visualize.dcgrph.draw_graph.kwargs`.
"""

nxgrph_visualize_tags = nts.AttributeGroupings('node_', 'edge_', 'legend_')
"""
:mod:`~tessif.visualize.nxgrph` attribute tags. Used as described in
:func:`~tessif.visualize.nxgrph.draw_graph`'s
:paramref:`~tessif.visualize.nxgrph.draw_graph.kwargs`. Using
:attr:`~tessif.frused.namedtuples.AttributeGroupings` for sub categorization
as well as easy to maintain and expand code.

Currently used tags:

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nxgrph_visualize_tags as nvt
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'nxgrph_visualize_tags.csv')

    df = pandas.DataFrame(data=nvt._asdict().values(),
                          index=nvt._asdict().keys())

    for row, value in enumerate(df[0]):
        df[0][row] = '{}{}{}'.format('``', value, '``')

    df.to_csv(path, header=None)

.. csv-table:: first column labels the namedtuples field
    :file: source/api/frused/defaults/nxgrph_visualize_tags.csv
    :stub-columns: 1
"""

nxgrph_visualize_xcptns = nts.AttributeGroupings(
    # node exceptions
    ['node_size', 'node_color', 'node_shape', 'node_fill_size'],
    # edge exceptions
    ['edge_labels', 'edge_color', 'edge_vmin', 'edge_vmax', 'edge_cmap'],
    # legend exceptions
    [])
"""
:mod:`~tessif.visualize.nxgrph` filter exceptions. Used as described in
:func:`~tessif.visualize.nxgrph.draw_graph`'s
:paramref:`~tessif.visualize.nxgrph.draw_graph.kwargs`. Using
:attr:`~tessif.frused.namedtuples.AttributeGroupings` for sub categorization
as well as easy to maintain and expand code.

Currently used exceptions:

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nxgrph_visualize_xcptns as nvx
    import pandas

    path = os.path.join(
         doc_dir, 'source', 'api', 'frused',
        'defaults', 'nxgrph_visualize_xcptns.csv')

    df = pandas.DataFrame(data=nvx._asdict().values(),
                          index=nvx._asdict().keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the namedtuples field
    :file: source/api/frused/defaults/nxgrph_visualize_xcptns.csv
    :stub-columns: 1
"""

nx_label_kwargs = {
    'nodes': [
        'ax', 'nodelist', 'node_size', 'node_fill_size', 'node_color',
        'node_shape', 'alpha', 'cmap', 'vmin', 'vmax', 'linewidts',
        'edgecolors', 'label'],
    'labels': [
        'labels', 'font_size', 'font_color',  'font_family', 'font_weight',
        'alpha', 'horizontalalignment', 'verticalalignment', 'ax'],
    'edges': [
        'edglist', 'width', 'edge_color', 'style', 'alpha', 'edge_cmap',
        'edge_vmin', 'edge_vmax', 'ax', 'arrows', 'arrowstyle', 'arrowsize',
        'connectionstyle', 'label', 'min_source_margin', 'min_target_margin',
        # following kwargs are needed for estimating edge size
        'node_shape', 'node_size', 'nodelist'
    ],
    'edge_labels': [
        'ax', 'alpha', 'edge_labels', 'label_pos', 'font_size', 'font_color',
        'font_weight', 'font_family', 'bbox', 'clip_on', 'horizontalalignment',
        'verticalalignment'],
}
"""
Registered :mod:`nxgrph.draw_graph <tessif.visualize.nxgrph.draw_graph>`
key word arguments keyed by respective sub drawing utility name. Used for
filtering out incompatible key word arguments. Explicitly stated
here for easily maintained and expanded code.

Currently used exceptions:

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nx_label_kwargs
    import pandas

    path = os.path.join(
         doc_dir, 'source', 'api', 'frused',
        'defaults', 'nx_label_kwargs.csv')

    df = pandas.DataFrame(data=nx_label_kwargs.values(),
                          index=nx_label_kwargs.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the keys
    :file: source/api/frused/defaults/nx_label_kwargs.csv
    :stub-columns: 1
"""


nx_label_kwargs = {
    'nodes': [
        'ax', 'nodelist', 'node_size', 'node_fill_size', 'node_color',
        'node_shape', 'alpha', 'cmap', 'vmin', 'vmax', 'linewidts',
        'edgecolors', 'label'],
    'labels': [
        'labels', 'font_size', 'font_color',  'font_family', 'font_weight',
        'alpha', 'horizontalalignment', 'verticalalignment', 'ax'],
    'edges': [
        'edglist', 'width', 'edge_color', 'style', 'alpha', 'edge_cmap',
        'edge_vmin', 'edge_vmax', 'ax', 'arrows', 'arrowstyle', 'arrowsize',
        'connectionstyle', 'label', 'min_source_margin', 'min_target_margin',
        # following kwargs are needed for estimating edge size
        'node_shape', 'node_size', 'nodelist'
    ],
    'edge_labels': [
        'ax', 'alpha', 'edge_labels', 'label_pos', 'font_size', 'font_color',
        'font_weight', 'font_family', 'bbox', 'clip_on', 'horizontalalignment',
        'verticalalignment'],
}
"""
Registered :mod:`nxgrph.draw_graph <tessif.visualize.nxgrph.draw_graph>`
key word arguments keyed by respective sub drawing utility name. Used for
filtering out incompatible key word arguments. Explicitly stated
here for easily maintained and expanded code.

Currently used exceptions:

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import nx_label_kwargs
    import pandas

    path = os.path.join(
         doc_dir, 'source', 'api', 'frused',
        'defaults', 'nx_label_kwargs.csv')

    df = pandas.DataFrame(data=nx_label_kwargs.values(),
                          index=nx_label_kwargs.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the keys
    :file: source/api/frused/defaults/nx_label_kwargs.csv
    :stub-columns: 1
"""

energy_system_nodes = {
    # Unique Identifiers
    'name': 'unspecified',
    'latitude': 0.0,
    'longitude': 0.0,
    'region': None,
    'sector': None,
    'carrier': None,
    'component': None,
    'node_type': None,
    'unspecified': 'Unspecified',

    # time serieses
    'timeseries': None,

    # singular values
    'accumulated_maximum': float('+inf'),
    'accumulated_minimum': 0.0,
    'active': 1,

    'characteristic_value': None,
    'costs_for_being_active': 0.0,

    'efficiency': 1.0,
    'emissions': 0.0,
    'exogenously_set': False,
    'exogenously_set_value': 0,
    'expandable': False,
    'fixed_expansion_ratios': True,
    'expansion_costs': 0.0,


    'flow_costs': 0.0,
    'final_soc': None,

    'gain_rate': 0.0,

    'initial_soc': 0.0,
    'initial_status': 1,
    'input': None,

    'interfaces': None,
    'installed_capacity': 0.0,

    'loss_rate': 0.0,

    'maximum': float('+inf'),
    'maximum_efficiency': 1.0,
    'maximum_expansion': float('+inf'),
    'maximum_flow_rate': float('+inf'),
    'maximum_shutdowns': float('+inf'),
    'maximum_startups': float('+inf'),

    'minimum': 0.0,
    'minimum_efficiency': 0.01,
    'minimum_expansion': 0.0,
    'minimum_flow_rate': 0.0,
    'minimum_downtime': 0,
    'minimum_uptime': 0,

    'negative_gradient': float('+inf'),
    'negative_gradient_costs': 0.0,

    'output': None,

    'positive_gradient': float('+inf'),
    'positive_gradient_costs': 0.0,

    'shutdown_costs': 0.0,
    'startup_costs': 0.0,
    'storage_capacity': 0.0,

    'variable_capacity': None,

    # chp values
    'chp_back_pressure': None,
    'chp_efficiency': {},
    'el_efficiency_wo_dist_heat': nts.MinMax(None, None),
    'enthalpy_loss': nts.MinMax(None, None),
    'min_condenser_load': None,
    'power_loss_index': None,
    'power_wo_dist_heat': nts.MinMax(None, None),

    # model specific
    'already_installed': 0.0,

    'back_pressure': False,

    'ideal': False,

    'milp': False,

    'number_of_connections': 1,

    'fine_region': 'Default Region'

}
"""
Fallback defaults for creating energy system nodes.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import energy_system_nodes
    import dutils

    df = dutils.to_dataframe(energy_system_nodes, columns=3, fillvalue='')

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'energy_system_nodes.csv')

    df.to_csv(path, header=None, index=None, na_rep='None')

.. csv-table::
    :file: source/api/frused/defaults/energy_system_nodes.csv
"""


registered_component_types = {
    'bus':
    ('bus',),
    'sink':
    ('sink', 'demand', 'export', 'excess',),
    'source':
    ('source', 'renewables', 'export', 'import', 'backup', 'commodity'),
    'storage':
    ('storage', 'generic_storage'),
    'transformer':
    ('transformer', 'mimo_transformer',),
    'connector':
    ('connector', 'link', 'line', 'connection',),
}
"""
Default energy system component identifiers and all types associated with them.

Used to :attr:`reorder <tessif.parse.reorder_esm>` an energy system mapping
during :mod:`parsing <tessif.parse>`.

Currently registered component types and their
:ref:`identifiers <Spellings_EnergySystemComponentIdentifiers>`.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import registered_component_types as rct
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'registered_component_types.csv')

    df = pandas.DataFrame(data=rct.values(),
                          index=rct.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the registration key
    :file: source/api/frused/defaults/registered_component_types.csv
    :stub-columns: 1
"""

addon_component_types = {
    'generic_chp': ('generic_chp',),
    'sito_flex_transformer': ('sito_flex_transformer',),
    'siso_nonlinear_transformer': (
        'offset_transformer', 'siso_nonlinear_transformer'),
}
"""
Added speciality energy system component identifiers and types associated with
them.

Currently registered component types and their
:ref:`identifiers <Spellings_EnergySystemComponentIdentifiers>` as added
components.

Note
----
Expand this dictionary when adding new speciality
:ref:`energy system components <Models_Tessif_Concept_ESC>` that are not quite
parseable using tessif's :ref:`approach <Models_Tessif_Concept>` but where a
specialised parsers exists or will be added. Like for example in
:meth:`tessif.transform.mapping2es.omf.generate_sito_flex_transformers`.


.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import addon_component_types as act
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'addon_component_types.csv')

    df = pandas.DataFrame(data=act.values(),
                          index=act.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the registration key
    :file: source/api/frused/defaults/addon_component_types.csv
    :stub-columns: 1
"""

registered_models = {
    'omf': spellings.oemof,
    'ppsa': spellings.pypsa,
    'fine': spellings.fine,
    'cllp': spellings.calliope,
}
"""
Registered energy supply system simulation models and their recognized
spelling variations.

.. execute_code::
    :hide_code:
    :hide_headers:
    :hide_output:

    from tessif.frused.paths import doc_dir
    import os
    from tessif.frused.defaults import registered_models as rm
    import pandas

    path = os.path.join(
        doc_dir, 'source', 'api', 'frused',
        'defaults', 'registered_models.csv')

    df = pandas.DataFrame(data=rm.values(),
                          index=rm.keys())

    df.to_csv(path, header=None)

.. csv-table:: first column labels the registration key
    :file: source/api/frused/defaults/registered_models.csv
    :stub-columns: 1


See Also
--------
:ref:`SupportedModels`
"""
# dash_visualize_defaults =
