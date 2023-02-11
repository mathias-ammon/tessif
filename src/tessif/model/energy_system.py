# src/tessif/model/energy_system.py
# pylint: disable=too-few-public-methods
"""Dummy energy_system module to enebale tessif-examples."""

# standard library
# import shutil
# import tempfile
# from pathlib import Path
import os
import pickle
import subprocess
import tempfile

# third pary packages
import pandas as pd

# local packages
import tessif.model.components as tessif_components
import tessif.frused.namedtuples as nts

uid_seperator = "_"

registered_plugins = {
    "oemof-4.4": "tessif-oemof-4.4",
    "omeof-latest": "tessif-oemof-4.4",
    "oemof": "tessif-oemof-4.4",
    "omf": "tessif-oemof-4.4",
}


class AbstractEnergySystem:
    """
    Aggregate tessif's abstract components into an energy system.

    Parameters
    ----------
    uid: ~collections.abc.Hashable
        Hashable unique identifier. Usually a string aka a name.
    busses: ~collections.abc.Iterable
        Iterable of :class:`~tessif.model.components.Bus`
        objects to be added to the energy system
    sinks: ~collections.abc.Iterable
        Iterable of :class:`~tessif.model.components.Sink`
        objects to be added to the energy system
    sources: ~collections.abc.Iterable
        Iterable of :class:`~tessif.model.components.Source`
        objects to be added to the energy system
    transformers: ~collections.abc.Iterable
        Iterable of
        :class:`~tessif.model.components.Transformer`
        objects to be added to the energy system
    storages: ~collections.abc.Iterable
        Iterable of
        :class:`~tessif.model.components.Storage`
        objects to be added to the energy system
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

    global_constraints: dict, default={'emissions': float('+inf')}
        Dictionary of :class:`numeric <numbers.Number>` values mapped to
        global constraint naming :class:`strings <str>`.

        Recognized constraint keys are:

            - ``emissions``
            - ...

        For a more detailed explanation see the user guide's section:
        :ref:`Secondary_Objectives`
    """

    def __init__(self, uid, *args, **kwargs):

        self._uid = uid

        kwargs_and_defaults = {
            'busses': (),
            'chps': (),
            'connectors': (),
            'sinks': (),
            'sources': (),
            'transformers': (),
            'storages': (),
            'timeframe': pd.Series(),
            'global_constraints': {'emissions': float('+inf')}}

        for kwarg, default in kwargs_and_defaults.copy().items():

            # overwrite default if user provided key word argument:
            kwargs_and_defaults[kwarg] = kwargs.get(kwarg, default)

            # initialize instance respective instance attribute:
            if kwarg == 'global_constraints':
                setattr(self, '_{}'.format(kwarg), kwargs_and_defaults[kwarg])

            elif kwarg != 'timeframe':
                setattr(self, '_{}'.format(kwarg),
                        tuple(kwargs_and_defaults[kwarg]))
            else:
                self._timeframe = kwargs_and_defaults[kwarg]

        self._es_attributes = tuple(kwargs_and_defaults.keys())

    def __repr__(self):
        return '{!s}({!r})'.format(self.__class__, self.__dict__)

    def __str__(self):
        return '{!s}(\n'.format(self.__class__) + ',\n'.join([
            *['    {!r}={!r}'.format(
                k.lstrip('_'), v) for k, v in self.__dict__.items()],
            ')'
        ])

    @property
    def uid(self):
        """:class:`~collections.abc.Hashable` unique identifier. Usually a
        string aka a name.
        """
        return self._uid

    @property
    def busses(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Bus` objects part
        of the energy system.
        """
        for bus in self._busses:
            yield bus

    @property
    def chps(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.CHP`
        objects part of the energy system.
        """
        for chp in self._chps:
            yield chp

    @property
    def connectors(self):
        """ :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Connectors` objects part
        of the energy system.
        """

        for connector in self._connectors:
            yield connector

    @property
    def sources(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Source` objects
        part of the energy system.
        """
        for source in self._sources:
            yield source

    @property
    def sinks(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Sink` objects part
        of the energy system.
        """
        for sink in self._sinks:
            yield sink

    @property
    def transformers(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Transformer`
        objects part of the energy system.
        """
        for transformer in self._transformers:
            yield transformer

    @property
    def storages(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Storage` objects
        part of the energy system.
        """
        for storage in self._storages:
            yield storage

    @property
    def nodes(self):
        """
        :class:`~collections.abc.Generator` yielding this energy system's
        components.
        """

        component_types = ['busses', 'chps', 'sources',
                           'sinks', 'transformers', 'storages',
                           'connectors']

        for component_type in component_types:
            for component in getattr(self, component_type):
                yield component

    @property
    def edges(self):
        """:class:`~collections.abc.Generator` of
        :class:`~tessif.frused.namedtuples.Edge`
        :class:`NamedTuples<typing.Namedtuple>` representing graph like `edges
        <https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#edge>`_.
        """
        # All edge information are stored inside the bus objects..
        for bus in self.busses:
            # Bus incoming edge should contain node.uid and bus.uid:
            for inflow in bus.inputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if inflow.split('.')[0] == node.uid.name:
                        edge = nts.Edge(str(node.uid), str(bus.uid))
                        yield edge

            # Bus leaving edges should contain bus.uid and node.uid:
            for outflow in bus.outputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if outflow.split('.')[0] == node.uid.name:
                        edge = nts.Edge(str(bus.uid), str(node.uid))
                        yield edge

        # ... except for the edges build by the connectors
        for connector in self.connectors:
            for inflow in connector.inputs:
                edge = nts.Edge(inflow, str(connector.uid))
                yield edge

            for outflow in connector.outputs:
                edge = nts.Edge(str(connector.uid), outflow)
                yield edge

    @property
    def global_constraints(self):
        """
        :class:`Dictionary <dict>` of :class:`numeric <numbers.Number>`
        values mapped to global constraint naming :class:`strings <str>`
        currently respected by the energy system.
        """
        return self._global_constraints

    def _edge_carriers(self):
        """
        Extract carrier information out of busses and connectors.
        """
        _ecarriers = {}
        # All edge information are stored inside the bus objects
        for bus in self.busses:
            # Bus incoming edge should contain node.uid and bus.uid:
            for inflow in bus.inputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if inflow.split('.')[0] == node.uid.name:
                        edge = nts.Edge(str(node.uid), str(bus.uid))
                        _ecarriers[edge] = inflow.split('.')[1]

            # Bus leaving edges should contain bus.uid and node.uid:
            for outflow in bus.outputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if outflow.split('.')[0] == node.uid.name:
                        edge = nts.Edge(str(bus.uid), str(node.uid))
                        _ecarriers[edge] = inflow.split('.')[1]

        for connector in self.connectors:
            for inflow in connector.inputs:
                for bus in self.busses:
                    if inflow == str(bus.uid):
                        edge = nts.Edge(inflow, str(connector.uid))
                        _ecarriers[edge] = list(bus.outputs)[0].split('.')[1]

            for outflow in connector.outputs:
                for bus in self.busses:
                    if outflow == str(bus.uid):
                        edge = nts.Edge(str(connector.uid), outflow)
                        _ecarriers[edge] = list(bus.inputs)[0].split('.')[1]

        return _ecarriers

    def connect(self, energy_system, connecting_busses, connection_uid):
        """Connect another :class:`AbstractEnergySystem` object to this one.

        Parameters
        ----------
        energy_system: tessif.model.energy_system.AbstractEnergySystem
            Energy system object to be connected to this energy system via the
            respective :paramref:`~connect_energy_systems.connecting_busses`.

            The :paramref:`energy_system's <connect.energy_system>`
            :class:`~tessif.model.components.Bus` specified in
            :paramref:`connecting_busses[1] <connect.connecting_busses>` will
            be connected to this energy system's
            :class:`~tessif.model.components.Bus` specified in
            :paramref:`connecting_busses[0] <connect.connecting_busses>`. So
            it's :attr:`~tessif.model.components.AbstractEsComponent.uid`
            must be found in this energy system.

        connecting_busses: ~collections.abc.tuple
            Tuple of :attr:`Uids <tessif.frused.namedtuples.Uid>` string
            representation specifying the busses with which the energy systems
            will be connected.

            The :paramref:`energy_system's <connect.energy_system>`
            :class:`~tessif.model.components.Bus` specified in
            :paramref:`connecting_busses[1] <connect.connecting_busses>` will
            be connected to this energy system's
            :class:`~tessif.model.components.Bus` specified in
            :paramref:`connecting_busses[0] <connect.connecting_busses>`.

        connection_uid: tessif.frused.namedtuples.Uid
            Uid of the :class:`~tessif.model.components.Connector` object
            created for connecting the energy system.


        Return
        ------
        tessif.model.energy_system.AbstractEnergySystem
            The energy system created by connecting the
            :paramref:`~connect.energy_system` to this energy system.
        """

        components_to_add = list()

        for component in energy_system.nodes:
            # is current component to be connected ?
            if not str(component.uid) == connecting_busses[1]:
                # no, so just prepare it for adding to the new es
                components_to_add.append(component)
            else:
                # yes it's to be connected, so create a connector:
                connector = tessif_components.Connector(
                    **connection_uid._asdict(),
                    interfaces=(connecting_busses[0],
                                connecting_busses[1]))

                components_to_add.append(connector)
                components_to_add.append(component)

        connected_es = self.from_components(
            uid=self.uid,
            timeframe=self.timeframe,
            global_constraints=self.global_constraints,
            components=set([*self.nodes, *components_to_add]))

        return connected_es

    def duplicate(self, prefix='', separator='_', suffix='copy'):
        """
        Duplicate the energy system and return it. Potentially modify
        the node names.

        Parameters
        ----------
        prefix: str, default=''
           String added to the beginning of every node's :attr:`Uid.name
           <tessif.frused.namedtuples.Uid>`, separated by
           :paramref:`~duplicate.seperator`.

        separator: str, default='_'
           String used for adding the :paramref:`~duplicate.prefix` and the
           :paramref:`~duplicate.suffix` to every node's :attr:`Uid.name
           <tessif.frused.namedtuples.Uid>`.

        suffix: str, default=''
           String added to the beginning of every node's :attr:`Uid.name
           <tessif.frused.namedtuples.Uid>`, separated by
           :paramref:`~duplicate.seperator`.
        """
        duplicated_nodes = list()
        for node in self.nodes:
            duplicated_nodes.append(node.duplicate(
                prefix=prefix,
                separator=separator,
                suffix=suffix))

        return self.from_components(
            uid=self.uid,
            components=duplicated_nodes,
            timeframe=self.timeframe,
            global_constraints=self.global_constraints)

    @property
    def timeframe(self):
        return self._timeframe

    def pickle(self, location):
        """Pickle this system model.

        Parameters
        ----------
        location: str, default = None
            String representing of a path the created system model is dumped
            to. Passed to: meth: `pickle.dump`.
        """
        pickle.dump(self.__dict__, open(location, "wb"))

    def unpickle(self, location):
        """Restore a pickled energy system object."""
        self.__dict__ = pickle.load(open(location, "rb"))

    def tropp(self, what=None, py="3.8", tool=None, version=None):
        """TRansform, Optimize and PostProcess this Tessif system model."""
        what = "oemof_4.4_3.8"

        if not tool:
            tool = what.split(uid_seperator)[0]
        if not version:
            tool_version = what.split(uid_seperator)[1]
        if not py:
            py = what.split(uid_seperator)[2]

        requested_plugin = f"{tool}-{tool_version}"
        registered_plugin = registered_plugins[requested_plugin]
        registered_plugin += "-python"

        with tempfile.TemporaryDirectory() as tempdir:

            system_model_location = os.path.join(
                tempdir, "tessif_system_model.tsf")
            self.pickle(system_model_location)

            subprocess.run(
                [
                    "nox",
                    "-f",
                    # try absolutifying once fully ported
                    "/home/tze/Matze/Codes/tsf_release/test_nox.py",
                    "-R",
                    "-s",
                    registered_plugin,
                    "--python",
                    "3.8",
                    "--",
                    system_model_location,
                ]
            )

    @classmethod
    def from_components(cls, uid, components, timeframe,
                        global_constraints={'emissions': float('+inf')},
                        **kwargs):
        """
        Create an energy system from a collection of component instances.

        Particularly usefull when creating energy systems out of existing ones.

        Parameters
        ----------
        uid: ~collections.abc.Hashable
            Hashable unique identifier. Usually a string aka a name.

        components: `~collections.abc.Iterable`
            Iterable of :mod:`tessif.model.components.AbstractEsComponent`
            objects the energy system will be created of.

        timeframe: pandas.DatetimeIndex, optional
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

        global_constraints: dict, default={'emissions': float('+inf')}
            Dictionairy of :class:`numeric <numbers.Number>` values mapped to
            global constraint naming :class:`strings <str>`.

            Recognized constraint keys are:

                - ``emissions``
                - ...

            For a more detailed explanation see the user guide's section:
            :ref:`Secondary_Objectives`

        Return
        ------
        :class:`AbstractEnergySystem`
            The newly constructed energy system containing each component
            found in :paramref:`~from_components.components`.
        """
        busses, chps, sinks, sources, transformers = [], [], [], [], []
        connectors, storages = [], []

        for c in components:
            if isinstance(c, tessif_components.Bus):
                busses.append(c)
            elif isinstance(c, tessif_components.CHP):
                chps.append(c)
            elif isinstance(c, tessif_components.Sink):
                sinks.append(c)
            elif isinstance(c, tessif_components.Source):
                sources.append(c)
            elif isinstance(c, tessif_components.Transformer):
                transformers.append(c)
            elif isinstance(c, tessif_components.Connector):
                connectors.append(c)
            elif isinstance(c, tessif_components.Storage):
                storages.append(c)

        es = AbstractEnergySystem(
            uid=uid,
            busses=busses,
            chps=chps,
            sinks=sinks,
            sources=sources,
            transformers=transformers,
            connectors=connectors,
            storages=storages,
            timeframe=timeframe,
            global_constraints=global_constraints,
        )

        return es

    # def to_nxgrph(self):
    #     """
    #     Transform the :class:`AbstractEnergySystem` object into a
    #     :class:`networkx.DiGraph` object.

    #     Return
    #     ------
    #     directional_graph: networkx.DiGraph
    #         Networkx Directional Graph representing the abstract energy system.
    #     """
    #     grph = nx.DiGraph(name=self._uid)
    #     for node in self.nodes:
    #         grph.add_node(
    #             str(node.uid),
    #             **node.attributes,
    #         )

    #     nxgrph.create_edges(grph, self.edges, carrier=self._edge_carriers())
    #     return grph
