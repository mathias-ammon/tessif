# tessif/frused/namedtuples
# -*- coding: utf-8 -*-
"""
:mod:`~tessif.frused.namedtuples` is a :mod:`tessif` subpackage aggregating
utility objects for cleaner and more verbose code in the context of naming
things.
"""
import collections
import typing
import tessif.frused.configurations as config


class UidBase(typing.NamedTuple):

    name: str
    latitude: float
    longitude: float
    region: str
    sector: str
    carrier: str
    component: str
    node_type: str

    def __str__(self):
        return config.node_uid_seperator.join(
            str(getattr(self, i)) for i in node_uid_styles[
                config.node_uid_style])


class Uid(UidBase):
    r"""
    **U**\ nique **ID**\ entifiers for each energy system component.

    Essential part of :ref:`tessif's labeling concept <Labeling_Concept>`.

    For an energy system component to be unique, the compination of the
    :ref:`uid components <Namedtuples_UidComponents>` beeing used must be
    unique. Which combination is used internally depends on on the used
    :attr:`node_uid_styles` which can be selected using
    :attr:`configurations.node_uid_style
    <tessif.frused.configurations.node_uid_style>`.

    :class:`~typing.NamedTuple` containing meta and geospatial information.

    Note
    ----
    Used for internal results mapping. See
    :attr:`~tessif.frused.configurations.node_uid_style` and
    :attr:`node_uid_styles` for more details.
    Especially when having issues with non-unique uid solver issues.

    Note
    ----
    A UID's components are the :ref:`Parameters <Namedtuples_UidComponents>`
    of this class. For recognized variations of these during data parsing
    see also: :ref:`Spellings_UidComponents`


    .. _Namedtuples_UidComponents:

    Parameters
    ----------
    name: str
        Identifier replacing the original label.
        i.e: 'PV', 'Gas_CHP', ...

    latitude: :class:`~numbers.Number`, default None
        Geospatial latitude in degree

    longitude: :class:`~numbers.Number`, default None
        Geospatial longitude in degree

    region: str, default None
        Arbitrary regional categorization string.
        'Europe', 'global', ...

    sector: str, default None
        Arbitrary sector categorization string.

    carrier: str, default None
        Arbitrary energy carrier categorization string.

    component: str, default None
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.

    node_type: str, default None
        Arbitrary node type categorization string.
        i.e. "Combined_Cycle", "Renewable", ...

    warning
    -------
    Uid component defaults have to be set manually, according to
    :attr:`defaults.energy_system_nodes
    <tessif.frused.defaults.energy_system_nodes>` to avoid circular imports!

    return
    ------
    uid: ~typing.NamedTuple
        Namedtuple instance object serving as uid
    """

    def __new__(cls, name,
                latitude=None,
                longitude=None,
                region=None,
                sector=None,
                carrier=None,
                component=None,
                node_type=None):
        self = super().__new__(cls, name,  latitude, longitude, region,
                               sector, carrier, component, node_type)

        return self

    @classmethod
    def reconstruct(cls, string_representation):
        """Reconstruct a :class:`Uid` from its :ref:`string representation
        <Labeling_Concept>`."""
        deconstructed_uid = string_representation.split(
            config.node_uid_seperator)
        dict_representation = dict()
        for pos, attr in enumerate(node_uid_styles[config.node_uid_style]):
            if pos > len(deconstructed_uid) - 1:
                msg = (
                    "Index out of range\n" +
                    "The node_uid_style specificiation needs to be done " +
                    "BEFORE constructing a Uid implying it also needs to be " +
                    "Done BEFORE CREATING a model specific energy system\n" +
                    "(Use 'qualname' before constructing the model specific " +
                    "energy system and use more specified styles before " +
                    "attempting a Uid reconstruction.)"
                )
                raise IndexError(msg)

            dict_representation[attr] = deconstructed_uid[pos]

        return cls(**dict_representation)


node_uid_styles = {
    'name': ['name'],
    'qualname': [i for i in Uid.__new__.__code__.co_varnames
                 if i not in ['self', 'cls']],
    'coords': ['name', 'latitude', 'longitude'],
    'region': ['name', 'region'],
    'sector': ['name', 'sector'],
    'carrier': ['name', 'carrier'],
    'component': ['name', 'component'],
    'node_type': ['name', 'node_type']}
"""
Provide possible internal node label representation styles. Use
:attr:`configurations.node_uid_style
<tessif.frused.configurations.node_uid_style>`. For selecting a particular
style.

Currently supported styles are (first column identifies the mapping key):

    .. execute_code::
        :hide_code:
        :hide_headers:
        :hide_output:

        import tessif.frused.namedtuples as nts
        from tessif.frused.paths import doc_dir
        import pandas as pd
        import os

        df = pd.DataFrame(
            index=nts.node_uid_styles.keys(),
            data=nts.node_uid_styles.values())

        path = os.path.join(
            doc_dir, 'source', 'api', 'frused',
            'namedtuples', 'node_uid_styles.csv')

        df.to_csv(path, header=None)

    .. csv-table::
        :file: source/api/frused/namedtuples/node_uid_styles.csv
        :stub-columns: 1

Combined with :attr:`~tessif.frused.configurations.node_uid_seperator`
a node of::

    lbl = tessif.frused.namedtuples.uid(
        name='test',
        latitude='lat',
        longitude='long',
        region='hamburg',
        sector='power',
        carrier='wind',
        component='source',
        node_type='renewable')

results into following representaion, depending on the mapping used:

    .. execute_code::
        :hide_code:
        :hide_headers:

        import tessif.frused.namedtuples as nts
        import tessif.frused.configurations as configs

        lbl = nts.Uid(
            name='test',
            latitude='lat',
            longitude='long',
            region='hamburg',
            sector='power',
            carrier='wind',
            component='source',
            node_type='renewable')

        nls = nts.node_uid_styles

        for key in nls.keys():
            configs.node_uid_style = key
            print(configs.node_uid_style, '->', lbl)
"""

Edge = collections.namedtuple('Edge', ['source', 'target'])
"""
Edge of an energy system graph. (source, target)

As of tessif's convention an Edge is describe as directional going from
``source`` to ``target``.

Parameters
----------
source: str
    :ref:`Uid representation <Labeling_Concept>` of the :ref:`energy system
    component <Models_Tessif_Concept_ESC>` representing the edges start.

target: str
    :ref:`Uid representation <Labeling_Concept>` of the :ref:`energy system
    component <Models_Tessif_Concept_ESC>` representing the edges end.
"""

MinMax = collections.namedtuple('MinMax', ['min', 'max'])
"""
Corespondent minimum and maximum value pair. Usually used for energy system
value parings like flow limits (i.e: minimum and maximum flow boundaries).
"""

OnOff = collections.namedtuple('OnOff', ['on', 'off'])
"""
Corespondent value pair for describing parameters dependent on a boolean
status. . Usually used for energy system value parings describing nonconvex
behaviour like i.e: minimum uptime and downtime.
"""

InOut = collections.namedtuple('InOut', ['inflow', 'outflow'])
"""
Corespondent inflow outflow value pair. Usually used for energy system value
parings describing different behaviours of the same component depending on in
or outflow like i.e: Storage efficiency
"""

PositiveNegative = collections.namedtuple(
    'PositiveNegative', ['positive', 'negative'])
"""
Corespondent value pair for describing parameters dependent on directions
expressed as positive or negative. Usually used for energy system value
parings describing changes between timesteps like i.e: power production
gradients.
"""

Coordinates = collections.namedtuple(
    'Coordinates', ['latitude', 'longitude'])
"""
Geospatial coordinates. (latitude [°], longitude[°])
"""


NodeColorGroupings = collections.namedtuple(
    'NodeColorGroupings',
    ['component', 'name', 'carrier', 'sector'])
"""
Node color groups mapped by format like
:class:`~tessif.transform.es2mapping.ESTransformer` objects.

Mapping colors are defined in :mod:`tessif.frused.themes`.
Unique energy system component identifier (:class:`uid`) parts are specified
in :attr:`~tessif.frused.spellings.energy_system_component_identifiers`.

Parameters
----------

component: defaultdict(list)
    Dictionairy of node colors with component searched for in
    :attr:`~tessif.frused.spellings.energy_system_component_identifiers`

label : defaultdict(list)
    Dictionairy of node colors with tags searched for in str(node.label)

carrier : defaultdict(list)
    Dictionairy of node colors with tags searched for in node.label.carrier

sector : defaultdict(list)
    Dictionairy of node colors with tags searched for in node.label.sector
"""


AttributeGroupings = collections.namedtuple(
    'AttributeGroupings',
    ['node', 'edge', 'legend'])
"""
Energy system graph attribute groupings. (Mainly used for filtering purposes).

Parameters
----------
node: str
    String to tag node related attributes
edge: str
    String to tag edge related attributes
legend: str
    String to tag legend related attributes

See also
--------
:paramref:`~tessif.visualize.nxgrph.draw_graph.kwargs`
parameter of :meth:`~tessif.visualize.nxgrph.draw_graph`

Implementation example:
:attr:`~tessif.frused.conventions.nxgrph_visualize_defaults`
"""

MemoryTime = collections.namedtuple(
    'MemoryTime',
    ['memory', 'time'])
"""
Simulation meta data result container. (Mainly used by
:class:`tessif.analye.Comparatier`).

Parameters
----------
memory: str
    String to tag memory related result data.
edge: str
    String to tag timing related result data.
"""

SimulationProcessStepResults = collections.namedtuple(
    'SimulationProcessStepResults',
    ['reading', 'parsing', 'transformation', 'simulation', 'post_processing', 'result'])
"""
Detailed meta data result container holding inrformation on the various
simulation process steps.

Parameters
----------
reading: ~numbers.Number
    Number representing the quantity needed for reading in the data
    during the simulation process.
parsing: ~numbers.Number
    Number representing the quantity needed for parsing the read in data
    during the simulation process.
transformation: ~numbers.Number
    Number representing the quantity needed for transforming the parsed
    data during the simulation process.
solving: ~numbers.Number
    Number representing the quantity needed for solving during the the
    simulation process.
post_processing: ~numbers.Number
    Number representing the quantity needed for post precessing the
    solving results during the simulation process.
"""

CLS = collections.namedtuple(
    "CLS",  # Correlate Line Style
    ["thresholds", "styles"],
)
"""Line style thresholds and style correlation.

See :paramref:`tessif.transform.es2mapping.base.EdgeFormatier.cls` for more
details.
"""
