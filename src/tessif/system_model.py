# src/tessif/energy_system.py
"""Tessifs energy supply syste model.

Serving as primary input data harmonization.

.. rubric:: Main Class/Functionality
.. autosummary::
   :nosignatures:

   AbstractEnergySystem
   AbstractEnergySystem.tropp

.. rubric:: Alternative Ways of Creation
.. autosummary::
   :nosignatures:

   AbstractEnergySystem.from_components

.. rubric:: Frequently Used Methods
.. autosummary::
   :nosignatures:

   AbstractEnergySystem.connect
   AbstractEnergySystem.duplicate
   AbstractEnergySystem.to_nxgrph

   AbstractEnergySystem.serialize
   AbstractEnergySystem.deserialize
   AbstractEnergySystem.pickle
   AbstractEnergySystem.unpickle
"""

import json

# standard library
import os
import pickle
import subprocess
import tempfile

import networkx as nx

# third pary packages
import pandas as pd

# local packages
import tessif.components as tessif_components
import tessif.frused.namedtuples as nts
from tessif import nxgraph
from tessif.deserialize import RestoredResults, SystemModelDecoder
from tessif.frused.defaults import registered_plugins
from tessif.frused.paths import tessif_dir
from tessif.serialize import SystemModelEncoder


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

        Currently recognized constraint keys are:

            - ``emissions``
    """

    def __init__(self, uid, *args, **kwargs):

        self._uid = uid

        kwargs_and_defaults = {
            "busses": (),
            "chps": (),
            "connectors": (),
            "sinks": (),
            "sources": (),
            "transformers": (),
            "storages": (),
            "timeframe": pd.Series(dtype="object"),
            "global_constraints": {"emissions": float("+inf")},
        }

        for kwarg, default in kwargs_and_defaults.copy().items():

            # overwrite default if user provided key word argument:
            kwargs_and_defaults[kwarg] = kwargs.get(kwarg, default)

            # initialize instance respective instance attribute:
            if kwarg == "global_constraints":
                setattr(self, f"_{kwarg}", kwargs_and_defaults[kwarg])

            elif kwarg != "timeframe":
                setattr(self, f"_{kwarg}", tuple(kwargs_and_defaults[kwarg]))
            else:
                self._timeframe = kwargs_and_defaults[kwarg]

        self._es_attributes = tuple(kwargs_and_defaults.keys())

    def __repr__(self):
        """Verbosify representation."""
        return f"{self.__class__!s}({self.__dict__!r})"

    def __str__(self):
        """Verbosify string representation."""
        return f"{self.__class__!s}(\n" + ",\n".join(
            [
                *[
                    "    {!r}={!r}".format(k.lstrip("_"), v)
                    for k, v in self.__dict__.items()
                ],
                ")",
            ]
        )

    _plurals_mapping = {
        "busses": "Bus",
        "chps": "CHP",
        "connectors": "Connector",
        "sinks": "Sink",
        "sources": "Source",
        "transformers": "Transformer",
        "storages": "Storage",
    }

    @property
    def uid(self):
        """:class:`~collections.abc.Hashable` unique identifier.

        Usually a string aka a name.
        """
        return self._uid

    @property
    def busses(self):
        """Generator of the system model's busses.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Bus` objects part
        of the energy system.
        """
        yield from self._busses

    @property
    def chps(self):
        """Generator of the system model's CHPs.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.CHP`
        objects part of the energy system.
        """
        yield from self._chps

    @property
    def connectors(self):
        """Generator of the system model's connectors.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Connectors` objects part
        of the energy system.
        """
        yield from self._connectors

    @property
    def sources(self):
        """Generator of the system model's sources.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Source` objects
        part of the energy system.
        """
        yield from self._sources

    @property
    def sinks(self):
        """Generator of the system model's sinks.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Sink` objects part
        of the energy system.
        """
        yield from self._sinks

    @property
    def transformers(self):
        """Generator of the system model's transformers.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Transformer`
        objects part of the energy system.
        """
        yield from self._transformers

    @property
    def storages(self):
        """Generator of the system model's storages.

        :class:`~collections.abc.Generator` of
        :class:`~tessif.model.components.Storage` objects
        part of the energy system.
        """
        yield from self._storages

    @property
    def nodes(self):
        """Generator yielding this system models' components."""
        component_types = [
            "busses",
            "chps",
            "sources",
            "sinks",
            "transformers",
            "storages",
            "connectors",
        ]

        for component_type in component_types:
            yield from getattr(self, component_type)

    @property
    def edges(self):
        """Generator yielding this system model's Graph representation edges.

        :class:`~collections.abc.Generator` of
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
                    if inflow.split(".")[0] == node.uid.name:
                        edge = nts.Edge(str(node.uid), str(bus.uid))
                        yield edge

            # Bus leaving edges should contain bus.uid and node.uid:
            for outflow in bus.outputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if outflow.split(".")[0] == node.uid.name:
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
        """The system model's global constraints.

        :class:`Dictionary <dict>` of :class:`numeric <numbers.Number>`
        values mapped to global constraint naming :class:`strings <str>`
        currently respected by the energy system.
        """
        return self._global_constraints

    def _edge_carriers(self):
        """Extract carrier information out of busses and connectors."""
        _ecarriers = {}
        # All edge information are stored inside the bus objects
        for bus in self.busses:
            # Bus incoming edge should contain node.uid and bus.uid:
            for inflow in bus.inputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if inflow.split(".")[0] == node.uid.name:
                        edge = nts.Edge(str(node.uid), str(bus.uid))
                        _ecarriers[edge] = inflow.split(".")[1]

            # Bus leaving edges should contain bus.uid and node.uid:
            for outflow in bus.outputs:
                # so find out node uid by string comparison with
                # every single node:
                for node in self.nodes:
                    if outflow.split(".")[0] == node.uid.name:
                        edge = nts.Edge(str(bus.uid), str(node.uid))
                        _ecarriers[edge] = inflow.split(".")[1]

        for connector in self.connectors:
            for inflow in connector.inputs:
                for bus in self.busses:
                    if inflow == str(bus.uid):
                        edge = nts.Edge(inflow, str(connector.uid))
                        _ecarriers[edge] = list(bus.outputs)[0].split(".")[1]

            for outflow in connector.outputs:
                for bus in self.busses:
                    if outflow == str(bus.uid):
                        edge = nts.Edge(str(connector.uid), outflow)
                        _ecarriers[edge] = list(bus.inputs)[0].split(".")[1]

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
                    interfaces=(connecting_busses[0], connecting_busses[1]),
                )

                components_to_add.append(connector)
                components_to_add.append(component)

        connected_es = self.from_components(
            uid=self.uid,
            timeframe=self.timeframe,
            global_constraints=self.global_constraints,
            components={*self.nodes, *components_to_add},
        )

        return connected_es

    def duplicate(self, prefix="", separator="_", suffix="copy"):
        """Duplicate the energy system and return it.

        Potentially modify the node names.

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
            duplicated_nodes.append(
                node.duplicate(prefix=prefix, separator=separator, suffix=suffix)
            )

        return self.from_components(
            uid=self.uid,
            components=duplicated_nodes,
            timeframe=self.timeframe,
            global_constraints=self.global_constraints,
        )

    @property
    def timeframe(self):
        """Timeframe representing the optimization time span."""
        return self._timeframe

    def serialize(self, fp=None):
        """Serialize this system model."""
        # prepare dictionairy
        serialized_dict = {}
        for attribute in self._es_attributes:

            # parse timeframe:
            if attribute == "timeframe":
                serialized_dict["timeframe"] = self.timeframe.to_series().to_json()

            # parse global constraints
            elif attribute == "global_constraints":
                serialized_dict["global_constraints"] = self.global_constraints

            # parse components:
            else:
                serialized_dict[attribute] = []
                for component in getattr(self, attribute):
                    serialized_dict[attribute].append(component.serialize())

        serialized_dict["uid"] = self.uid

        serialized_system_model = json.dumps(
            serialized_dict,
            cls=SystemModelEncoder,
        )

        return serialized_system_model

    @classmethod
    def deserialize(cls, stream):
        """Load from stored system."""
        system_dict = json.loads(stream)
        for attribute_name, value in system_dict.copy().items():

            # deserialize uid
            if attribute_name == "uid":
                system_dict["uid"] = value

            # deserialize timeframe
            elif attribute_name == "timeframe":
                dct = json.loads(value)
                # datetime index was serialized using a pandas series
                datetimeindex_in_ms = tuple(dct.keys())

                # recreate datetimeindex using "ms" which Series.to_json uses
                index = pd.to_datetime(datetimeindex_in_ms, unit="ms")
                freq = pd.infer_freq(index)

                # Use the inferred frequency to restore the DatetimeIndex object
                # with its original frequency
                restored_index = pd.date_range(start=index[0], end=index[-1], freq=freq)
                system_dict["timeframe"] = restored_index

            elif attribute_name == "global_constraints":
                system_dict["global_constraints"] = value

            else:
                list_of_jsoned_component_attributes = value
                # map "busses" to bus, etc
                component_type = cls._plurals_mapping[attribute_name]
                system_dict[attribute_name] = []

                for component_attributes in list_of_jsoned_component_attributes:
                    system_dict[attribute_name].append(
                        # recreate tessif components using "form_attributes"
                        getattr(tessif_components, component_type).from_attributes(
                            json.loads(component_attributes, cls=SystemModelDecoder)
                        )
                    )

        return cls(**system_dict)

    def pickle(self, location):
        """Pickle this system model.

        Parameters
        ----------
        location: str, default = None
            String representing of a path the created system model is pickled
            to. Passed to: meth: `pickle.dump`.
        """
        pickle.dump(self.__dict__, open(location, "wb"))

    def unpickle(self, location):
        """Restore a pickled energy system object."""
        self.__dict__ = pickle.load(open(location, "rb"))

    def tropp(
        self, plugins, trans_ops=None, opt_ops=None, quiet=False, parent_dir=None
    ):
        """Transform, Optimize and PostProcess this Tessif system model.

        Parameters
        ----------
        plugins:
            Iterable of plugin strings used for tropping.
        trans_ops : dict, None
            Dictionairy of transformation options.
        opt_ops : dict, None
            Dictionairy of optimization options.
        quite : bool
            If True tropp logging level is set to logging.WARNING
        parent_dir : str, None
            Parent directory aka tessif's main user directory. Usually
            established using ``tessif init my_parent_dir``. If default
            initialization is used (``tessif init`` recommended) then the main
            user directory
            is ``~/.tessif.d/`` and this parameter can and should be ignored.

        Returns
        -------
        dict
            Dictionairy holding the :class:`tessif.deserialize.RestoredResults`
            keyed by:

            - "igr" for the restored integrated global results (restored
              :class:`tessif.post_process.IntegratedGlobalResultier` like)
            - "alr" for the the of the restored results (restored AllResultier
              like)
        """
        # Sanitize Plugins
        sanitized_plugins = []

        for plugin in plugins:
            if plugin not in registered_plugins.keys():
                pass
            else:
                sanitized_plugins.append(registered_plugins[plugin])

        # parse working directory
        if not parent_dir:
            parent_dir = tessif_dir

        tropp_results = {}
        for rgstrd_plgn in sanitized_plugins:
            tropp_results[rgstrd_plgn] = {}

            # use a temporary directory to pickle and unpickle system models
            # and results
            with tempfile.TemporaryDirectory() as tempdir:

                # store the system model to disk, so it can be reloaded inside
                # the pluging virtual environment
                system_model_location = os.path.join(tempdir, "tessif_system_model.tsf")

                serialized_sys_mod = self.serialize()

                json.dump(
                    serialized_sys_mod,
                    fp=open(system_model_location, "w"),
                )

                venv_dir = os.path.join(parent_dir, "plugin-venvs", rgstrd_plgn)
                activation_script = os.path.join(venv_dir, "bin", "activate")

                activation_command = f". {activation_script}; "
                # tropp_command = f"tessif tropp --directory {tempdir} {rgstrd_plgn}"
                tropp_command = " ".join(
                    [
                        "tessif",
                        "tropp",
                        "--directory",
                        tempdir,
                        rgstrd_plgn,
                    ]
                )

                if quiet:
                    tropp_command = " ".join([tropp_command, "--quiet"])

                if trans_ops:
                    tropp_command = " ".join(
                        [tropp_command, "--trans_ops", f"'{json.dumps(trans_ops)}'"]
                    )

                subprocess.run(
                    activation_command + tropp_command,
                    shell=True,
                    check=True,
                )

                deserialized_results = json.loads(
                    json.load(
                        open(
                            os.path.join(tempdir, f"{rgstrd_plgn}_all_resutlier.alr"),
                        )
                    )
                )

                tropp_results[rgstrd_plgn]["alr"] = RestoredResults(
                    deserialized_results
                )

                deserialized_results = json.loads(
                    json.load(
                        open(
                            os.path.join(tempdir, f"{rgstrd_plgn}_igr_resultier.igr"),
                        ),
                    ),
                )

                tropp_results[rgstrd_plgn]["igr"] = RestoredResults(
                    deserialized_results
                )

        return tropp_results

    @classmethod
    def from_components(
        cls,
        uid,
        components,
        timeframe,
        global_constraints=None,
        **kwargs,
    ):
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

        Return
        ------
        :class:`AbstractEnergySystem`
            The newly constructed energy system containing each component
            found in :paramref:`~from_components.components`.
        """
        if not global_constraints:
            global_constraints = {"emissions": float("+inf")}

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

    def to_nxgrph(self):
        """Transform tessif system model into networkx graph.

        Transform the :class:`AbstractEnergySystem` object into a
        :class:`networkx.DiGraph` object.

        Return
        ------
        directional_graph: networkx.DiGraph
            Networkx Directional Graph representing the abstract energy system.
        """
        grph = nx.DiGraph(name=self._uid)
        for node in self.nodes:
            grph.add_node(
                str(node.uid),
                **node.attributes,
            )

        nxgraph.create_edges(grph, self.edges, carrier=self._edge_carriers())
        return grph
