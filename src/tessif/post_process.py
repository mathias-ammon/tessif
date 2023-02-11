"""Tessif's Post Processing Template and Utilitiy.

Transforming (optimized) energy systems to `mappings
<https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_.

:class:`ESTransformer` defines  an abstract base
class serving as template. Down the lineage the energy system transformer
family then divides into a triangular like structure:

    1. A :class:`Resultier`
       branch which is a set of classes being responsible for extracting
       result like information and mapping them to the respective
       :ref:`node uid string representation <Labeling_Concept>`. They serve as
       interface to post processing utilities further down the chain.

    2. A :class:`Formatier <NodeFormatier>`
       branch which is a set of classes being responsible for generating
       format like information and mapping them to the respective
       :ref:`node uid string representation <Labeling_Concept>`.

       They are all descendants of resultiers. They serve as
       interface for visualizing utilities further down the post processing
       chain.

    3. A :class:`Hybridier <ICRHybridier>` branch which combines specific
       result and format results mapped to
       :ref:`node uid string representations <Labeling_Concept>`.

       They serve as specific post processing routines mainly for developing
       certain kinds of diagrams. See for example the :class:`ICRHybridier`
       in conjunction with :attr:`tessif.analyze.Comparatier.ICR_graphs`.
"""
import abc
import collections
import inspect
import logging
from collections import defaultdict
from itertools import cycle
from math import copysign

import matplotlib as mpl
import numpy as np
import pandas as pd

from tessif.frused import configurations as configs
from tessif.frused import defaults
from tessif.frused import namedtuples as nts
from tessif.frused import spellings, themes, utils

logger = logging.getLogger(__name__)
esci = spellings.energy_system_component_identifiers


class ESTransformer(abc.ABC):
    """
    Abstract base class for the energy system transformer family.

    All attributes needed to ensure framework compatibility are exposed here.
    Takes an optimized energy system instance and works its magic on it.

    Calls:

        - :func:`_map_nodes`
        - :func:`_map_edges`

    Parameters
    ----------
    optimized_es : energy_system
        Object returned a supported energy system simulation library. See
        :ref:`SupportedModels` for a list of supported energy system simulation
        tools.
    """

    #: Dictionary of node and edge attribute defaults. Used by all attribute
    #: aggregating utilities throughout this framework to fill in attribute
    #: defaults instead of None.
    defaults = {}

    def __init__(self, optimized_es, **kwargs):
        """ """
        self._nodes = self._map_nodes(optimized_es)
        self._node_uids = self._map_node_uids(optimized_es)
        self._edges = self._map_edges(optimized_es)

    @abc.abstractmethod
    def _map_nodes(self, optimized_es):
        """
        Class internal function designed to extract data interpretative as
        :attr:`~networkx.Graph.nodes` out of the optimized energy system to be
        transformed.

        This function needs to be filled with
        :paramref:`~_map_nodes.optimized_es` specific logic. It therefore was
        chosen to be made abstract.

        Parameters
        ----------
        optimized_es : energy_system
            Object returned by the energy system simulation library. See
            :ref:`SupportedModels` for a list of supported energy system
            simulation tools.

        Return
        ------
        nodes : :class:`collections.abc.Iterable`
            Iterable of nodes

        Note
        ----
        When overriding this function in a subclass, do provide a docstring
        otherwise you gonna see this again. ;)

        Make sure your overridden version returns an iterable of nodes.
        Otherwise you break the :mod:`~tessif.transform.es2mapping` concept.

        """

    @abc.abstractmethod
    def _map_node_uids(self, optimized_es):
        """
        Class internal function designed to extract data interpretative as
        :attr:`~networkx.Graph.nodes` out of the optimized energy system to be
        transformed.

        This function needs to be filled with
        :paramref:`~_map_nodes.optimized_es` specific logic. It therefore was
        chosen to be made abstract.

        In contrast to :meth:`_map_nodes` this function maps the actual
        :ref:`node uids <Labeling_Concept>`, which can be useful for advanced
        operations or models not supporting a uid concept natively.

        Parameters
        ----------
        optimized_es : energy_system
            Object returned by the energy system simulation library. See
            :ref:`SupportedModels` for a list of supported energy system
            simulation tools.

        Return
        ------
        nodes : :class:`collections.abc.Iterable`
            Iterable of nodes

        Note
        ----
        When overriding this function in a subclass, do provide a docstring
        otherwise you gonna see this again. ;)

        Make sure your overridden version returns an iterable of nodes.
        Otherwise you break the :mod:`~tessif.transform.es2mapping` concept.

        """

    @abc.abstractmethod
    def _map_edges(self, optimized_es):
        """
        Class internal function designed to extract data interpretative as
        :attr:`~networkx.Graph.nodes` out of the optimized energy system to be
        transformed.

        This function needs to be filled with
        :paramref:`~_map_edges.optimized_es` specific logic. It therefore was
        chosen to be made abstract.

        Parameters
        ----------
        optimized_es : energy_system
            Object returned by the energy system simulation library.
            See :attr:`~tessif.transform.es2mapping.base.supported` for a list
            of supported energy system simulation tools.

        Return
        ------
        edges : :class:`collections.abc.Iterable`
            Iterable of edges

        Note
        ----
        When overriding this function in a subclass, do provide a docstring
        otherwise you gonna see this again. ;)

        Make sure your overridden version returns an iterable of edges.
        Otherwise you break the :mod:`~tessif.transform.es2mapping` concept.

        """

    @property
    def nodes(self):
        """:class:`~collections.abc.Container` of energy system component
        string representations interpretable as nodes."""
        return self._nodes

    @property
    def uid_nodes(self):
        """:class:`~collections.abc.Mapping` of energy system component uids
        (interpretable as nodes) to their
        :ref:`node uid string representation <Labeling_Concept>`.
        """
        return self._node_uids

    @property
    def edges(self):
        """:class:`~collections.abc.Container` of energy system component
        string representations interpretable as edges."""
        return self._edges

    @property
    def inbounds(self):
        """:class:`~collection.abc.Mapping` of a list of inbound nodes
        (in fact their uid string representations) to the node (in fact its
        uid string representations) being the target of the inbounds.

        Meaning, for an energy system like ``1 -> 2 <-3``, this mapping would
        look like ::

            inbounds['1'] == []
            inbounds['2'] == ['1', '3']

        """
        _inbounds = defaultdict(list)
        for node in self.nodes:
            for edge in self.edges:
                if node == edge.target:
                    _inbounds[node].append(edge.source)

        return _inbounds

    @property
    def outbounds(self):
        """:class:`~collection.abc.Mapping` of a list of outbound nodes
        (in fact their uid string representations)
        to the node (in fact its uid string representations) being the source
        of the outbounds.

        Meaning, for an energy system like ``1 <- 2 -> 3``, this mapping would
        look like ::

            outbounds['1'] == []
            outbounds['2'] == ['1', '3']

        """
        _outbound = defaultdict(list)
        for node in self.nodes:
            for edge in self.edges:
                if node == edge.source:
                    _outbound[node].append(edge.target)

        return _outbound

    def node_data(self):
        r"""
        Function to get a ready to use dictionary of node attribute names and
        parameters as expected by other utilities throughout this framework.

        Return
        ------
        attributes: dict
            Dictionary of node attributes and parameters as generated by this
            object provided all node attributes are of type :class:`property`
            and contain **node_** as well as not contain **_node** in its
            name.

            Refer to :class:`XmplResultier` to see how this implementation
            works out.

        Note
        ----
        This assumes the naming convention is honored in that all node
        attributes are properties and contain **node_** as well as not
        contain **_node** in their name. In fact being properties is not
        really necessary but a good practice anyways though.

        """
        # get all attributes of this instance as a list of (name, value):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        # get all attributes starting with node_ but not _node
        node_attribute_names = list(
            a[0] for a in attributes if "node_" in a[0] and "_node" not in a[0]
        )
        # return dict of node attrs ready to be used by i.e nxgraph.Graph
        return {
            attr_name: getattr(self, attr_name) for attr_name in node_attribute_names
        }

    def edge_data(self):
        r"""
        Function to get a ready to use dictionary of edge attribute names and
        parameters as expected by other utilities throughout tessif.

        Return
        ------
        attributes: dict
            Dictionary of edge attributes and parameters as generated by this
            object provided all edge attributes are of type :class:`property`
            and contain **edge_** as well as not contain **_edge** in its
            name.

            Refer to :class:`XmplResultier` to see how this implementation
            works out.

        Note
        ----
        This assumes the naming convention is honored in that all edge
        attributes are properties and contain **edge_** as well as not
        contain **_edge** in their name. In fact being properties is not
        really necessary but a good practice anyways though.

        """
        # edge data should not consist of attributes having following tags
        excluding = ["_edge", "edge_data"]
        # edge data should consist of attributes having following tags
        including = ["edge_"]

        # aggregate edge attribute names
        _edge_data = list()
        for attr in dir(self):
            if any(include in attr for include in including) and not any(
                exclude in attr for exclude in excluding
            ):

                _edge_data.append(attr)

        return {attr_name: getattr(self, attr_name) for attr_name in _edge_data}

        # get all attributes of this instance as a list of (name, value):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))

        # get all attributes starting with edge_ but not _edge
        edge_attribute_names = list(
            a[0] for a in attributes if "edge_" in a[0] and "_edge" not in a[0]
        )

        return {
            attr_name: getattr(self, attr_name) for attr_name in edge_attribute_names
        }


class XmplResultier(ESTransformer):
    r"""
    An exemplary resultier like child of :class:`ESTransformer`.

    Serves as show case on how to use Resultier type objects when
    interfacing with other utilities in this framework. Often
    used in doctest like examples throughout the project. Therefor
    it needs to be independent of an optimized energy system.
    (Which is totally not what this family of classes is all about)

    See :class:`OmfNetResultier` for a real use case example.

    Example
    --------
    Recreating the :class:`XmplResultier` to demonstrate a minimum working
    example. See the respective documentation below this example.

    >>> from tessif.transform.es2mapping.base import ESTransformer
    >>> class XmplResultier2(ESTransformer):
    ...     def __init__(self, optimized_es=None):
    ...         super().__init__(optimized_es=optimized_es)
    ...         self._node_attr_xmpl = 'red'
    ...         self._edge_attr_xmpl = {
    ...            edge: sum(tuple(map(int, edge))) for edge in self.edges}
    ...
    ...     def _map_nodes(self, optimized_es):
    ...         return ['1', '2', '3']
    ...
    ...     def _map_node_uids(self, optimized_es):
    ...         return ['1', '2', '3']
    ...
    ...     def _map_edges(self, optimized_es):
    ...         return [('1', '2'),  ('2', '3'), ('3', '1')]
    ...
    ...     @property
    ...     def node_attr_xmpl(self):  return self._node_attr_xmpl
    ...
    ...     @property
    ...     def edge_attr_xmpl(self): return self._edge_attr_xmpl
    ...
    >>> XR = XmplResultier2()
    >>> print(XR.nodes)
    ['1', '2', '3']
    >>> print(XR.edges)
    [('1', '2'), ('2', '3'), ('3', '1')]
    >>> print(XR.node_data())
    {'node_attr_xmpl': 'red'}
    >>> print(XR.edge_data())
    {'edge_attr_xmpl': {('1', '2'): 3, ('2', '3'): 5, ('3', '1'): 4}}
    """

    def __init__(self, optimized_es=None, **kwargs):
        r"""
        Standard :class:`XmplResultier` initializer.

        It does not care about the optimized energy system and creates
        arbitrary nodes and edges as well as an exemplary attribute for each
        node and some edges. All of those creations are done explicitly and do
        **not** reflect the design purpose (which of course shouldn't stop you
        abusing this class:) ).

        Calls:

            - :func:`ESTransformer.__init__`

        Note
        ----
        The :func:`~ESTransformer._map_nodes` and
        :func:`~ESTransformer._map_edges` functions are called when the super
        constructor is called.

        """
        super().__init__(optimized_es=optimized_es, **kwargs)
        self._node_attr_xmpl = "red"
        self._edge_attr_xmpl = {edge: sum(tuple(map(int, edge))) for edge in self.edges}

    def _map_nodes(self, optimized_es):
        r"""Return an exemplary :class:`~collections.abc.Iterable` of nodes"""
        return ["1", "2", "3"]

    def _map_node_uids(self, optimized_es):
        r"""Return an exemplary :class:`~collections.abc.Iterable` of nodes"""
        return ["1", "2", "3"]

    def _map_edges(self, optimized_es):
        r"""Return an exemplary :class:`~collections.abc.Iterable` of edges"""
        return [("1", "2"), ("2", "3"), ("3", "1")]

    @property
    def node_attr_xmpl(self):
        r"""Exemplary node attribute. Makes every node red.

        Note
        ----
        Remember that :func:`~ESTransformer.node_data` only detects attributes
        containing **node_** and not containing **_node** in their name.
        """
        return self._node_attr_xmpl

    @property
    def edge_attr_xmpl(self):
        r"""Exemplary edge attribute. Calculates the sum of the edge nodes.
        Emulates ":paramref:`~ESTransformer.optimized_es` dependent logic"

        Note
        ----
        Remember that :func:`~ESTransformer.edge_data` only detects attributes
        containing **edge_** and not containing **_edge** in their name.

        """
        return self._edge_attr_xmpl


class Resultier(ESTransformer):
    """Transform nodes and edges into their name representation. Child of
    ESTransformer and  mother of all model specific resultiers.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.
    """

    def __init__(self, optimized_es, **kwargs):

        super().__init__(optimized_es=optimized_es, **kwargs)

    @abc.abstractmethod
    def _map_nodes(self, optimized_es):
        pass

    @abc.abstractmethod
    def _map_edges(self, optimized_es):
        pass


class IntegratedGlobalResultier(Resultier):
    """
    Extracting the integrated global results out of the energy system and
    conveniently aggregating them (rounded to unit place) inside a dictionary
    keyed by result name.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    LoadResultier children like, e.g..:
    :class:`es2mapping.omf.IntegratedGlobalResultier
    <tessif.transform.es2mapping.omf.IntegratedGlobalResultier>`.
    """

    def __init__(self, optimized_es, **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)

        self._global_results = self._map_global_results(optimized_es)

    @property
    def global_results(self):
        """
        Integrated global results (IGR) mapped by result name.

        Integrated global results currently consist of meta and non-meta
        results. the **meta** results are handled by the:mod:`~tessif.analyze`
        module and consist of:

            - ``time``
            - ``memory``

        results, whereas the **non-meta** results consist of:

            - ``emissions``
            - ``costs``

        results. The befornamed strings serve as key inside the mapping.
        """
        return self._global_results

    @abc.abstractmethod
    def _map_global_results(self, optimized_es):
        """Interface to extract the integrated global results out of the
        :ref:`model <SupportedModels>` specific, optimized energy system and
        map them to their result names (``costs``, ``emissions``, ``time``,
        ``memory``)

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.IntegratedGlobalResultier` source code
        for exemplary implementation.
        """
        pass


class LoadResultier(Resultier):
    """
    Transforming flow results into dictionaries keyed by node.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    LoadResultier children like, e.g..: :class:`es2mapping.omf.LoadResultier
    <tessif.transform.es2mapping.omf.LoadResultier>`.
    """

    def __init__(self, optimized_es, **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)
        self._node_loads = self._map_loads(optimized_es)
        self._inflows = self._map_inflows()
        self._outflows = self._map_outflows()
        self._loads_old = self._map_summed_loads()

    @property
    def node_load(self):
        """Timeseries flow results mapped to their
        :ref:`node uid representation <Labeling_Concept>`.

        Mapped are :class:`pandas.DataFrame` objects containing:

            - Inbound flows as negative values
            - Outbound flows as positive values
            - The mapped-to :ref:`node uid representation <Labeling_Concept>`
              as ``pandas.DataFrame.columns.name``
            - In- or outbound :ref:`node uid representation <Labeling_Concept>`
              as :attr:`column names <pandas.DataFrame.columns>`
        """
        sorted_loads = dict()
        for node, load in self._node_loads.items():
            # sort bus dataframe to first show inputs and then show outputs
            inflows, outflows = pd.DataFrame(), pd.DataFrame()
            for (columnName, columnData) in load.items():
                # copysign(1, i) returns 1 if i > 0 or i == +0.0 and returns -1
                # if i < 0 or i == -0.0
                if all(copysign(1, i) > 0 for i in columnData.values):
                    outflows[columnName] = columnData
                elif all(copysign(1, i) < 0 for i in columnData.values):
                    inflows[columnName] = columnData

            # sort inflow and outflow alphabetically
            inflows.sort_index(axis=1, inplace=True)
            # print(outflows)
            # print(node)
            outflows.sort_index(axis=1, inplace=True)

            # reassamble the data frame
            df = pd.concat([inflows, outflows], axis="columns")

            # name the index column
            df.columns.name = load.columns.name

            sorted_loads[node] = df

        return sorted_loads

    @property
    def node_inflows(self):
        """Incoming timeseries flow results as positive values mapped
        to their :ref:`node uid representation <Labeling_Concept>`.

        Mapped are :class:`pandas.DataFrame` objects containing:

            - The mapped-to :ref:`node uid representation <Labeling_Concept>`
              as ``pandas.DataFrame.columns.name``
            - Inbound :ref:`node uid representation <Labeling_Concept>`
              as :attr:`column names <pandas.DataFrame.columns>`
        """
        return self._inflows

    @property
    def node_outflows(self):
        """Outgoing timeseries flow results as positive values mapped
        to their :ref:`node uid representation <Labeling_Concept>`.

        Mapped are :class:`pandas.DataFrame` objects containing:

            - The mapped-to :ref:`node uid representation <Labeling_Concept>`
              as ``pandas.DataFrame.columns.name``
            - Outbound :ref:`node uid representation <Labeling_Concept>`
              as :attr:`column names <pandas.DataFrame.columns>`
        """
        return self._outflows

    @property
    def node_summed_loads(self):
        """Summed timeseries flow results mapped to their
        :ref:`node uid representation <Labeling_Concept>`.

        Mapped are :class:`pandas.Series` objects containing:

            - Inbound flows as positive values for sinks
            - Outbound flows as positive values for all other components
        """
        return self._loads_old

    def _map_inflows(self):
        """Interface to extract inflow results out of the :ref:`model
        <SupportedModels>` specific, optimized energy system and map them to
        their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Does NOT need to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.LoadResultier` for exemplary
        implementation.
        """
        _inflow_loads = defaultdict(lambda: pd.DataFrame())
        for node, load in self.node_load.items():

            # only keep negative  values and make em positive
            # df = -1 * load[load < 0].fillna(-0.)
            df = -1 * load[np.copysign(1.0, load) < 0].dropna(axis="columns")

            # kick out any duplicate columns
            new_df = pd.DataFrame()
            for col_name, series in df.items():
                if df.columns.to_list().count(col_name) > 1 and (series <= 0).all():
                    pass
                else:
                    new_df[col_name] = series

            # add all 0 inflow nodes in case they were kicked out
            for inbound in self.inbounds[node]:
                if inbound not in new_df.columns:
                    new_df[inbound] = 0.0

            # kick out not outflow nodes
            for column in new_df.columns:
                if column not in self.inbounds[node]:
                    new_df.drop(column, axis="columns", inplace=True)

            # copy the name to new df
            new_df.columns.name = df.columns.name

            # sort columns alphabetically
            _inflow_loads[str(node)] = new_df.sort_index(axis="columns")

        return dict(_inflow_loads)

    @abc.abstractmethod
    def _map_loads(self, optimized_es):
        """Interface to extract in- and outflow results out of the :ref:`model
        <SupportedModels>` specific, optimized energy system and map them to
        their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.LoadResultier` for exemplary
        implementation.
        """

    def _map_outflows(self):
        """Interface to extract in- and outflow results out of the :ref:`model
        <SupportedModels>` specific, optimized energy system and map them to
        their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Does NOT need to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.LoadResultier` for exemplary
        implementation.
        """
        _outflow_loads = defaultdict(lambda: pd.DataFrame())
        for node, load in self.node_load.items():

            # only keep positive values
            # df = load[load > 0].fillna(0)
            # df = load[np.copysign(1.0, load) > 0].fillna(0)
            df = load[np.copysign(1.0, load) > 0].dropna(axis="columns")

            # kick out any duplicate columns
            new_df = pd.DataFrame()
            for col_name, series in df.items():
                if df.columns.to_list().count(col_name) > 1 and (series <= 0).all():
                    pass
                else:
                    new_df[col_name] = series

            # add all-0 outflow nodes in case they were kicked out
            for outbound in self.outbounds[node]:
                if outbound not in new_df.columns:
                    new_df[outbound] = 0.0

            # only keep the actual outflow nodes
            for column in new_df.columns:
                if column not in self.outbounds[node]:
                    new_df.drop(column, axis="columns", inplace=True)

            # copy the name to new df
            new_df.columns.name = df.columns.name

            # sort columns alphabetically

            _outflow_loads[str(node)] = new_df.sort_index(axis="columns")
        return dict(_outflow_loads)

    def _map_summed_loads(self):
        """Interface to extract in- and outflow results out of the :ref:`model
        <SupportedModels>` specific, optimized energy system and map them tools
        their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Does NOT need to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.LoadResultier` for exemplary
        implementation.
        """
        _summed_loads = defaultdict(lambda: pd.DataFrame())
        for representation, uid in self.uid_nodes.items():
            if uid.component in spellings.sink:
                series = self.node_inflows[representation].sum(axis="columns")
            else:
                series = self.node_outflows[representation].sum(axis="columns")

            _summed_loads[representation] = series

        return dict(_summed_loads)


class CapacityResultier(Resultier):
    r"""Transforming installed capacity results dictionaries keyed by node.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    reference_capacity: ~numbers.Number, None default=None
        Number to externally set reference capacity.
        If ``None`` (default) maximum installed capacity is used.

    kwargs:
        Key word arguments are passed to :class:`Resultier`.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    CapacityResultier children like, e.g..:
    :class:`es2mapping.omf.CapacityResultier
    <tessif.transform.es2mapping.omf.CapacityResultier>`.
    """

    def __init__(self, optimized_es, **kwargs):

        # Parse reference capacity out of kwargs to not influence
        # the chain of inheritance
        if "reference_capacity" in kwargs:
            reference_capacity = kwargs.pop("reference_capacity")
        else:
            reference_capacity = None

        super().__init__(optimized_es=optimized_es, **kwargs)

        # do the mapping
        self._installed_capacities = self._map_installed_capacities(optimized_es)
        self._original_capacities = self._map_original_capacities(optimized_es)

        self._expansion_costs = self._map_expansion_costs(optimized_es)

        self._characteristic_values = self._map_characteristic_values(optimized_es)
        self._reference_capacity = self._map_reference_capacity(
            reference=reference_capacity
        )

    @property
    def node_installed_capacity(self):
        r"""Installed capacities of the energy system components mapped to
        their :ref:`node uid representation <Labeling_Concept>`.

        Components of variable size have an installed capacity as stated in
        :attr:`tessif.frused.defaults.energy_system_nodes`.

        :math:`P_{cap}= \text{installed capacity}`
        """
        return self._installed_capacities

    @property
    def node_original_capacity(self):
        r"""Installed pre-optimization capacities of the energy system
        components mapped to their
        :ref:`node uid representation <Labeling_Concept>`.

        Components of variable size have an installed capacity as stated in
        :attr:`tessif.frused.defaults.energy_system_nodes`.

        :math:`P_{origcap}= \text{installed capacity}`
        """
        return self._original_capacities

    @property
    def node_expansion_costs(self):
        r"""Installed capacity expansion costs for components mapped to their
        :ref:`node uid representation <Labeling_Concept>`.
        """
        return self._expansion_costs

    @property
    def node_characteristic_value(self):
        r"""Characteristic values of the energy system components mapped to
        their :ref:`node uid representation <Labeling_Concept>`.

        Components of variable size or have a characteristic value as stated in
        :attr:`tessif.frused.defaults.energy_system_nodes`.

        Characteristic value in this context means:

            - :math:`cv = \frac{\text{characteristic flow}}
              {\text{installed capacity}}` for:

                - :class:`~tessif.model.components.Source` objects
                - :class:`~tessif.model.components.Sink` objects
                - :class:`~tessif.model.components.Transformer` objects

            - :math:`cv = \frac{\text{mean}\left(\text{SOC}\right)}
              {\text{capacity}}` for:

                - :class:`~tessif.model.components.Storage`


        Characteristic flow in this context means:

            - ``mean(`` :attr:`LoadResultier.node_summed_loads` ``)``

                - :class:`~tessif.model.components.Source` objects
                - :class:`~tessif.model.components.Sink` objects

            - ``mean(0th outflow)`` for:

                - :class:`~tessif.model.components.Transformer` objects

        The **node fillsize** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **characteristic value**.
        If no capacity is defined (i.e for nodes of variable size, like busses
        or excess sources and sinks, node size is set to it's default (
        :attr:`nxgrph_visualize_defaults[node_fill_size]
        <tessif.frused.defaults.nxgrph_visualize_defaults>`).
        """
        return self._characteristic_values

    @property
    def node_reference_capacity(self):
        """
        The systems reference capacity, most often used as scaling factor.

        Usually the highest installed capacity throughout the energy system.
        """
        return self._reference_capacity

    @property
    def load_resultier(self):
        """
        :ref:`Model <SupportedModels>` specific :class:`LoadResultier`, used
        for calculating the :attr:`characteristic values
        <node_characteristic_value>`.
        """
        return self._loads

    @abc.abstractmethod
    def _map_installed_capacities(self, optimized_es):
        """Interface to extract installed capacity results out of the
        :ref:`model<SupportedModels>` specific, optimized energy system and map
        them to their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.CapacityResultier` source code for
        exemplary implementation.
        """
        pass

    @abc.abstractmethod
    def _map_characteristic_values(self, optimized_es):
        """Interface to extract installed capacity and flow results out of the
        :ref:`model <SupportedModels>` specific, optimized energy system to
        calculate a characteristic value for each component and map this value
        the respective component's :ref:`node uid representation
        <Labeling_Concept>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.CapacityResultier` source code for
        exemplary implementation.
        """
        pass

    def _map_reference_capacity(self, reference=None):

        if reference is None:
            capacities = [
                v for v in self.node_installed_capacity.values() if v is not None
            ]
            flattened_capacities = list()
            for item in capacities:
                if isinstance(item, collections.abc.Iterable):
                    for component in item:
                        if component is not None:
                            flattened_capacities.append(component)
                else:
                    flattened_capacities.append(item)

            reference_capacity = max(flattened_capacities)

        else:
            reference_capacity = reference

        return reference_capacity


class StorageResultier(Resultier):
    r"""Transforming storage results into dictionaries keyed by node.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    StorageResultier children like, e.g..:
    :class:`es2mapping.omf.StorageResultier
    <tessif.transform.es2mapping.omf.StorageResultier>`.
    """

    def __init__(self, optimized_es, **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)
        self._states_of_charge = self._map_states_of_charge(optimized_es)

    @property
    def node_soc(self):
        """:ref:`Node uid representation <Labeling_Concept>` to state of
        charge (soc)  mapping for all storages of the energy system.
        """
        return self._states_of_charge

    def _map_states_of_charge(self, optimized_es):
        """Interface to extract the state of charge results out of the
        :ref:`model <SupportedModels>` specific, optimized energy system and
        map them to their :ref:`node uid representation <Labeling_Concept>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.StorageResultier` source code for
        exemplary implementation.
        """
        pass


class NodeCategorizer(Resultier):
    r"""Categorizing the nodes of an optimized oemof energy system.

    Categorization utilizes :attr:`~tessif.frused.namedtuples.Uid`.

    Nodes are categorized by:

        - Energy :paramref:`component
          <tessif.frused.namedtuples.Uid.component>`
          (One of the :ref:`energy system component identifiers
          <Models_Tessif_Concept_ESC>` 'Bus', 'Sink', etc..)

        - Energy :paramref:`sector <tessif.frused.namedtuples.Uid.sector>`
          ('power', 'heat', 'mobility', 'coupled')

        - :paramref:`Region <tessif.frused.namedtuples.Uid.region>`
          ('arbitrary label')

        - :paramref:`Coordinates <tessif.frused.namedtuples.Uid.latitude>`
          (latitude, longitude in degree)

        - Energy :paramref:`carrier <tessif.frused.namedtuples.Uid.carrier>`
          ('solar', 'wind', 'electricity', 'steam' ...)

        - :paramref:`Node type <tessif.frused.namedtuples.Uid.node_type>`
          ('arbitrary label')

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    NodeCategorizer children like, e.g.:
    :class:`es2mapping.omf.NodeCategorizer
    <tessif.transform.es2mapping.omf.NodeCategorizer>`.
    """

    def __init__(self, optimized_es, **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)

        self._map_node_groups()
        self._map_node_categories()

    groupings = {
        "components": "component",
        "energy_carriers": "carrier",
        "node_types": "node_type",
        "regions": "region",
        "sectors": "sector",
    }
    """
    Groupings used to generate mappings of
    :class:`~tessif.frused.namedtuples.Uid` attributes. Meaning for
    ``components: component`` a property called ``component_grouped`` will be
    generated using the :paramref:`~tessif.frused.namedtuples.Uid.component`
    attribute.
    """

    categories = {"coordinates": ["latitude", "longitude"], "carriers": ["carrier"]}
    """
    Categories of attributes that are mapped directly to each
    :ref:`node uid representation <Labeling_Concept>` of the energy system.

    Meaning for an energy system like ``1 -> 2 <-3``, this mapping could
    look like ::

            {'1': 'wind',
             '2': 'electricity',
             '3': 'solar'}

    for the :paramref:`~tessif.frused.namedtuples.Uid.carrier` category.
    """

    abbrevations = {
        "Ac": "AC",
        "Dc": "DC",
    }

    def _map_node_groups(self):
        """
        Group :ref:`node uid representation <Labeling_Concept>`
        by keys specified in :attr:`groupings` and make them
        accessible as respective attribute.

        Meaning for each key in :attr:`groupings` their will be a
        NodeCategorizer attribute of this name representing a dictionary
        with the values of :attr:`groupings` as key mapping the
        :ref:`node uid representation <Labeling_Concept>` according
        to their respective uid component.
        """
        for group, uid_attribute in self.groupings.items():
            group_dict = defaultdict(list)

            for representation, uid in self.uid_nodes.items():
                c = getattr(uid, uid_attribute)
                if c == defaults.energy_system_nodes[uid_attribute]:
                    group_dict[defaults.energy_system_nodes["unspecified"]].append(
                        representation
                    )
                else:
                    key = c.lower().capitalize()
                    for wrong_abbrv, right_abbrv in self.abbrevations.items():
                        if wrong_abbrv in key:
                            key = key.replace(wrong_abbrv, right_abbrv)

                    group_dict[key].append(representation)

            setattr(self, f"_{group}", dict(group_dict))

    def _map_node_categories(self):
        """
        Create a mapping for every node to each attribute categorised
        in :attr:`categories`.
        """
        for category, uid_attribute_list in self.categories.items():
            category_dict = defaultdict(list)

            for representation, uid in self.uid_nodes.items():
                node_category_values = [
                    getattr(uid, attr) for attr in uid_attribute_list
                ]

                if len(node_category_values) == 1:
                    node_category_values = node_category_values[0]

                if category == "coordinates":
                    node_category_values = nts.Coordinates(*node_category_values)

                category_dict[representation] = node_category_values

            setattr(self, f"_{category}", dict(category_dict))

    @property
    def node_components(self):
        """:ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>` of each node
        present in the energy system mapped to their `node uid representation
        <Labeling_Concept>`.
        """
        return self._components

    @property
    def node_coordinates(self):
        """:paramref:`Latitude <tessif.frused.namedtuples.Uid.latitude>` and
        :paramref:`~tessif.frused.namedtuples.Uid.longitude` of each node
        present in the energy system mapped to their `node uid representation
        <Labeling_Concept>`.
        """
        return self._coordinates

    @property
    def node_region_grouped(self):
        """:ref:`Node uid representations <Labeling_Concept>` grouped by
        :paramref:`~tessif.frused.namedtuples.Uid.region`
        (i.e "World" "South" "Antinational").
        """
        return self._regions

    @property
    def node_sector_grouped(self):
        """
        :ref:`Node uid representations <Labeling_Concept>` of the nodes present
        in the energy system grouped by energy
        :paramref:`~tessif.frused.namedtuples.Uid.sector` (i.e "Power" "Heat"
        "Mobility" "Coupled").
        """
        return self._sectors

    @property
    def node_type_grouped(self):
        """:ref:`Node uid representations <Labeling_Concept>` of the energy
        system's nodes grouped by
        :paramref:`~tessif.frused.namedtuples.Uid.node_type` (arbitrary
        classification, i.e. "Combined_Cycle", "Renewable", ...)
        """
        return self._node_types

    @property
    def node_carrier_grouped(self):
        """:ref:`Node uid representations <Labeling_Concept>` of the energy
        system's nodes grouped by energy
        :paramref:`~tessif.frused.namedtuples.Uid.carrier`. (i.e.
        "Electricity", "Gas", "Water").
        """
        return self._energy_carriers

    @property
    def node_energy_carriers(self):
        """Energy :paramref:`~tessif.frused.namedtuples.Uid.carrier` mapped to
        the :ref:`node uid representations <Labeling_Concept>` of the nodes
        present in the energy system.
        """
        return self._carriers


class FlowResultier(Resultier):
    """
    Transforming flow results into dictionaries keyed by edges.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    See also
    --------
    For examples check one of the :ref:`model <SupportedModels>` specific
    FlowResultier children like, e.g.:
    :class:`es2mapping.omf.FlowResultier
    <tessif.transform.es2mapping.omf.FlowResultier>`.
    """

    def __init__(self, optimized_es, **kwargs):
        # Parse reference emissions and net energy flow out of kwargs to not
        # influence the chain of inheritance
        if "reference_emissions" in kwargs:
            reference_emissions = kwargs.pop("reference_emissions")
        else:
            reference_emissions = None

        if "reference_net_energy_flow" in kwargs:
            reference_net_energy_flow = kwargs.pop("reference_net_energy_flow")
        else:
            reference_net_energy_flow = None

        super().__init__(optimized_es=optimized_es, **kwargs)

        # do the mapping
        self._net_energy_flows = self._map_net_energy_flows(optimized_es)
        self._specific_flow_costs = self._map_specific_flow_costs(optimized_es)
        self._specific_emissions = self._map_specific_emissions(optimized_es)
        self._edge_weights = self._map_edge_weights()
        self._edge_len = self._map_edge_lens()

        # map reference values
        self._reference_net_energy_flow = self._map_reference_net_energy_flow(
            reference=reference_net_energy_flow
        )
        self._reference_emissions = self._map_reference_emissions(
            reference=reference_emissions
        )

    @property
    def edge_net_energy_flow(self):
        r"""
        Time integrated flow results mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`\sum\limits_{t} \text{flow}\left(Edge\right)`
        """
        return self._net_energy_flows

    @property
    def edge_total_costs_incurred(self):
        r"""
        Energy specific flow costs mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`c_{\text{flow}}` ins
        :math:`\frac{\text{cost unit}}{\text{energy unit}}`
        """
        incurred_costs = {}
        for edge in self.edges:
            ics = self._specific_flow_costs[edge] * self.edge_net_energy_flow[edge]
            incurred_costs[edge] = ics

        return incurred_costs

    @property
    def edge_total_emissions_caused(self):
        r"""
        Energy specific emissions mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`e_{\text{flow}}` in
        :math:`\frac{\text{emission unit}}{\text{energy unit}}`
        """
        emissions_caused = {}
        for edge in self.edges:
            ics = self.edge_specific_emissions[edge] * self.edge_net_energy_flow[edge]
            emissions_caused[edge] = ics

        return emissions_caused

    @property
    def edge_specific_flow_costs(self):
        r"""
        Energy specific flow costs mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`c_{\text{flow}}` in
        :math:`\frac{\text{cost unit}}{\text{energy unit}}`
        """
        return self._specific_flow_costs

    @property
    def edge_specific_emissions(self):
        r"""
        Energy specific emissions mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`e_{\text{flow}}` in
        :math:`\frac{\text{emission unit}}{\text{energy unit}}`
        """
        return self._specific_emissions

    @property
    def edge_weight(self):
        r"""
        Edge weights mapped to the respective
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Edges are weighed by specific costs, scaled by maximum costs present.
        The more expensive, the heavier.

        Edge weights can for example be used during :func:`visualization
        <tessif.visualize.nxgrph.draw_graphical_representation>` or for finding
        `shortest paths
        <https://networkx.github.io/documentation/stable/reference/algorithms/shortest_paths.html>`_
        .

        See also
        --------
        `Weighted Graph
        <https://networkx.github.io/documentation/networkx-1.9/examples/drawing/weighted_graph.html>`_

        `Random use cases of weighted edges
        <https://www.quora.com/What-does-a-weight-on-edges-represent-in-a-weighted-graph-in-graph-theory?share=1>`_

        `Shortest path algorithm using networkx
        <https://testfixsphinx.readthedocs.io/en/latest/reference/generated/networkx.algorithms.shortest_paths.weighted.single_source_dijkstra_path_length.html>`_
        """
        return self._edge_weights

    @property
    def edge_len(self):
        return self._edge_len

    @property
    def edge_reference_emissions(self):
        """Reference emissions."""
        return self._reference_emissions

    @property
    def edge_reference_net_energy_flow(self):
        """Reference net energy flow."""
        return self._reference_net_energy_flow

    def _map_net_energy_flows(self, optimized_es):
        """
        Interface for mapping the integrated energy flows (summed up over all
        timesteps) to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`.
        """
        _net_energy_flows = defaultdict(float)
        for node in self.nodes:
            for inflow in self.node_inflows[node].columns:
                _net_energy_flows[nts.Edge(inflow, node)] = round(
                    self.node_inflows[node][inflow].sum(axis="index"), 2
                )

        return dict(_net_energy_flows)

    @abc.abstractmethod
    def _map_specific_flow_costs(self, optimized_es):
        """Interface for mapping the specific flow cost results to their
        respective :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.FlowResultier
        <tessif.transform.es2mapping.omf.FlowResultier>` source code for
        exemplary implementation.
        """
        pass

    @abc.abstractmethod
    def _map_specific_emissions(self, optimized_es):
        """Interface for mapping the specific flow emission results to their
        respective :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.FlowResultier
        <tessif.transform.es2mapping.omf.FlowResultier>` source code for
        exemplary implementation.
        """

        pass

    def _map_edge_weights(self):
        """Interface for mapping edge weights  to their
        respective :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Edges are weighed by specific costs, scaled by maximum costs present.
        The more expensive, the more weight.
        """
        # Use default dict as edge weights container:
        _edge_weights = defaultdict(float)
        max_costs = max(self._specific_flow_costs.values())

        # Map the respective edge weights:
        if max_costs > 0:
            for key in self._specific_flow_costs.keys():

                _edge_weights[key] = self.edge_specific_flow_costs[key] / max_costs

                if (
                    _edge_weights[key]
                    < defaults.nxgrph_visualize_defaults["edge_minimum_weight"]
                ):
                    _edge_weights[key] = defaults.nxgrph_visualize_defaults[
                        "edge_minimum_weight"
                    ]

        else:
            for key in self._specific_flow_costs.keys():
                _edge_weights[key] = defaults.nxgrph_visualize_defaults[
                    "edge_minimum_weight"
                ]

        return dict(_edge_weights)

    def _map_edge_lens(self):
        """Interface for mapping edge weights  to their
        respective :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Edges length are scaled by edge weight. The more weight, the longer.
        """
        return self._edge_weights

    def _map_reference_emissions(self, reference):
        if reference is None:
            reference_emissions = max(self.edge_specific_emissions.values())
            if reference_emissions == 0:
                reference_emissions = 1
        else:
            reference_emissions = reference

        return reference_emissions

    def _map_reference_net_energy_flow(self, reference):
        if reference is None:
            reference_net_energy_flow = max(self.edge_net_energy_flow.values())
        else:
            reference_net_energy_flow = reference

        return reference_net_energy_flow


class LabelFormatier(Resultier):
    """
    Generate component summaries as multiline label dictionary entries.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.
    """

    def __init__(self, optimized_es, **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)

        # mappings
        self._node_summaries = self._map_node_labels()
        self._edge_summaries = self._map_edge_labels()

    @property
    def node_summaries(self):
        r"""Multiline node summary strings mapped to their
        :ref:`node uid representation <Labeling_Concept>`. Useful for
        certain on-the-fly
        debug / testing applications. (See
        :meth:`tessif.visualize.nxgrph.draw_numerical_representation`)

        Summary consists of:

            - :attr:`Name <tessif.model.components.AbstractESComponent.name>`
            - :attr:`Installed capacity
              <CapacityResultier.node_installed_capacity>` :math:`P_{cap}`
            - :attr:`Characteristic value
              <CapacityResultier.node_characteristic_value>` :math:`C_f`

        """
        return self._node_summaries

    @property
    def edge_summaries(self):
        r"""Multiline edge summary strings mapped to their
        :class:`~tessif.frused.namedtuples.Edge` Useful for
        certain on-the-fly  debug/testing applications. (See
        :meth:`tessif.visualize.nxgrph.draw_numerical_representation`)

        Summary consists of:

            - :attr:`Net energy flow <FlowResultier.edge_net_energy_flow>`
              :math:`\sum\limits_t`
            - :attr:`Specific flow costs
              <FlowResultier.edge_specific_flow_costs>` :math:`c_{\text{flow}}`
            - :attr:`Specific emissions <FlowResultier.edge_net_energy_flow>`
              :math:`e_{\text{flow}}`

        """
        return self._edge_summaries

    def _map_node_labels(self):
        r"""Interface for mapping node result summaries to their respective
        :ref:`node uid representation <Labeling_Concept>`.

        Summarized are:

            - :attr:`Name <tessif.model.components.AbstractESComponent.name>`
            - :attr:`Installed capacity
              <CapacityResultier.node_installed_capacity>` :math:`P_{cap}`
            - :attr:`Characteristic value
              <CapacityResultier.node_characteristic_value>` :math:`C_f`
        """
        # Use default dict of str as node labels container
        _node_labels = defaultdict(str)

        # Map the respective node labels:
        for node in self.nodes:
            inst_cap = self.node_installed_capacity[node]
            characteristic_value = self.node_characteristic_value[node]

            # distinguish between singular and multiple inst capacities:
            if not isinstance(inst_cap, collections.abc.Iterable):

                # inst cap is singular; is it None?
                if inst_cap and characteristic_value:
                    # no, so proceed processing..

                    # storage nodes capacity differ form every other node type
                    if getattr(self.uid_nodes[node], "component") in spellings.storage:

                        _node_labels[node] = {
                            node: "{}\n{:.0f} {}h\ncv: {:.1f}".format(
                                node,
                                inst_cap,
                                configs.power_reference_unit,
                                characteristic_value,
                            )
                        }
                    else:
                        _node_labels[node] = {
                            node: "{}\n{:.0f} {}\ncf: {:.1f}".format(
                                node,
                                inst_cap,
                                configs.power_reference_unit,
                                characteristic_value,
                            )
                        }

                # yes it is None, so set it to variable size.
                else:
                    _node_labels[node] = {node: f"{node}\n var"}

            # inst capacities has multiple values
            else:
                _node_labels[node] = {
                    node: "{}\n{} {}\ncf: {}".format(
                        node,
                        list(inst_cap.values),
                        configs.power_reference_unit,
                        list(characteristic_value.values),
                    )
                }

        return dict(_node_labels)

    def _map_edge_labels(self):
        r"""
        Interface for mapping edge result summaries to their
        respective :class:`Edges <tessif.frused.namedtuples.Edge>`.

        Summarized are:

            - :attr:`Net energy flow <FlowResultier.edge_net_energy_flow>`
              :math:`\sum\limits_t`
            - :attr:`Specific flow costs
              <FlowResultier.edge_specific_flow_costs>` :math:`c_{\text{flow}}`
            - :attr:`Specific emissions <FlowResultier.edge_net_energy_flow>`
              :math:`e_{\text{flow}}`
        """
        # Use default dict as edge labels container:
        _edge_labels = defaultdict(str)

        # Map the respective edge labels:
        for edge in self.edges:

            if not any(
                [self.uid_nodes[node].component in spellings.storage for node in edge]
            ):
                net_flow = self.edge_net_energy_flow[edge]
                flow_costs = self.edge_specific_flow_costs[edge]
                emissions = self.edge_specific_emissions[edge]

                _edge_labels[(edge.source, edge.target)] = {
                    (
                        edge.source,
                        edge.target,
                    ): "{:.0f} {}h\n{:.1f} {}/{}h\n{:.1f} t/{}h".format(
                        # net energy flow
                        net_flow,
                        configs.power_reference_unit,
                        # flow costs
                        flow_costs,
                        configs.cost_unit,
                        configs.power_reference_unit,
                        # emissions
                        emissions,
                        configs.power_reference_unit,
                    )
                }
            else:

                net_flow = (
                    self.edge_net_energy_flow[edge]
                    + self.edge_net_energy_flow[(edge.target, edge.source)]
                )

                flow_costs = (
                    self.edge_specific_flow_costs[edge]
                    + self.edge_specific_flow_costs[(edge.target, edge.source)]
                )

                emissions = (
                    self.edge_specific_emissions[edge]
                    + self.edge_specific_emissions[(edge.target, edge.source)]
                )

                _edge_labels[(edge.source, edge.target)] = {
                    (
                        edge.source,
                        edge.target,
                    ): "{:.0f} {}h\n{:.1f} {}/{}h\n{:.1f} t/{}h".format(
                        # net energy flow
                        net_flow,
                        configs.power_reference_unit,
                        # flow costs
                        flow_costs,
                        configs.cost_unit,
                        configs.power_reference_unit,
                        # emissions
                        emissions,
                        configs.power_reference_unit,
                    )
                }

        return dict(_edge_labels)


class MplLegendFormatier(Resultier):
    r"""
    Generating visually enhanced matplotlib legends for nodes and edges.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    cgrp: str, default='name'
        Which group of color attribute(s) to return. One of::

            {'name', 'carrier', 'sector'}

        Color related attributes are grouped by
        :class:`tessif.frused.namedtuples.NodeColorGroupings` and are thus
        returned as a :class:`typing.NamedTuple`. Certain api functionalities
        expect those attributes to be dicts. (Usually those working only
        on :class:`~tessif.transform.es2mapping.base.ESTransformer` input).
        Use this parameter on Formatier creation to provide the expected
        dictionary.

    markers: str, default='formatier'
        What marker to use for legend entries. Either ``'formatier'`` or
        one of the :any:`matplotlib.markers`.

        If ``'formatier'`` is used, markers will be inferred from
        :attr:`NodeFormatier.node_shape`.
    """

    def __init__(self, optimized_es, cgrp="all", markers="formatier", **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)

        self._cgrp = cgrp
        self._markers = markers
        self._node_legend = self._create_node_legend()
        self._node_style_legend = self._create_node_style_legend()
        self._edge_style_legend = self._create_edge_style_legend()

    @property
    def node_legend(self):
        r"""
        Color grouped matplotlib legend attributes mapped to their parameter.

        Grouping utilizes
        :attr:`~tessif.frused.namedtuples.NodeColorGroupings`.
        Available groupings are:

            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.label`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.carrier`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.sector`
        """
        grp = self._cgrp
        if grp == "all":
            return self._node_legend
        elif grp in self._node_legend._fields:
            return getattr(self._node_legend, grp)
        else:
            logger.warning(f"Tried to access nonexistent field {grp} from {__name__}.")
            logger.warning(
                "Use 'all' or one of the existing fields: {}".format(
                    nts.NodeColorGroupings._fields
                )
            )
            logger.warning("Returning default group")
            return self._node_legend.name

    @property
    def node_style_legend(self):
        """Matplotlib legend attributes mapped to their parameters to describe
        :paramref:`fency node styles
        <tessif.visualize.nxgrph.draw_nodes.draw_fency_nodes>`. Fency as in:

            - variable node size being outer fading circles
            - cycle filling being proportional capacity factors
            - outer diameter being proportional installed capacities
        """
        return self._node_style_legend

    @property
    def edge_style_legend(self):
        """Matplotlib legend attributes mapped to their parameters to describe
        the chosen edge style. Current style represents:

            - net energy flow being proportional to edge width
            - specific_emissions being proportional to darkness
            - specific flow costs being proportional to edge length
        """
        return self._edge_style_legend

    def _create_node_legend(self):
        """
        Create a 3 legend tuple of nodes grouped by label sector and carrier.

        Each legend consists of a dict filled with matplotlib.Legend kwargs.

        """
        # Use a defaultdict of str as legend kwargs container:
        _component_grouped_node_color_legend = defaultdict(str)
        _label_grouped_node_color_legend = defaultdict(str)
        _carrier_grouped_node_color_legend = defaultdict(str)
        _sector_grouped_node_color_legend = defaultdict(str)

        # Empty marker and label lists filled in the process
        legend_markers = list()
        legend_entries = list()

        # Energy component sorted legend
        for component, color in themes.colors.component.items():
            if color in self._nformats.node_color.component.values():
                node_marker = mpl.lines.Line2D(
                    [],
                    [],
                    marker="o",
                    markerfacecolor=color,
                    markeredgecolor=color,
                    markersize=15,
                    linestyle="",
                )
                legend_markers.append(node_marker)
                legend_entries.append(component)

        _component_grouped_node_color_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "Component Type Colorings",
            "legend_bbox_to_anchor": (1.0, 0.5),
            "legend_loc": "center left",
            "legend_borderaxespad": 0,
        }

        # clear marker and label lists:
        legend_markers = []
        legend_entries = []

        # Label sorted legend
        for node in sorted(self.nodes):
            color = self._nformats.node_color.name[node]

            if self._markers == "formatier":
                marker = self._nformats.node_shape[node]
            else:
                marker = self._markers
            if self._nformats.node_size[node] == "variable":

                most_outer_circle = mpl.lines.Line2D(
                    [],
                    [],
                    marker=marker,
                    markerfacecolor=color,
                    alpha=0.3,
                    markeredgecolor=color,
                    linestyle="",
                    markersize=15,
                )

                outer_circle = mpl.lines.Line2D(
                    [],
                    [],
                    marker=marker,
                    markerfacecolor=color,
                    alpha=0.6,
                    markeredgecolor=color,
                    markersize=10,
                    linestyle="",
                )

                inner_circle = mpl.lines.Line2D(
                    [],
                    [],
                    marker=marker,
                    markerfacecolor=color,
                    markeredgecolor=color,
                    markersize=5,
                    linestyle="",
                )

                legend_markers.append((most_outer_circle, outer_circle, inner_circle))
                legend_entries.append(node)
            else:
                # scale node size with installed capacity:
                outer_circle_size = 15
                # self.node_size[str(
                #    node.label)] / self.defaults['node_size'] * 15

                base_size = self.node_characteristic_value[node]
                if isinstance(base_size, collections.abc.Iterable):
                    # use the minimum characteristic value, for a
                    # pessimistic estimation
                    base_size = min(base_size)

                cap_inner_circle = mpl.lines.Line2D(
                    [],
                    [],
                    marker=marker,
                    markerfacecolor=color,
                    markeredgecolor=color,
                    linestyle="",
                    markersize=base_size * 15,
                )

                cap_outer_circle = mpl.lines.Line2D(
                    [],
                    [],
                    marker=marker,
                    markerfacecolor="white",
                    markeredgecolor=color,
                    linestyle="",
                    markersize=outer_circle_size,
                )

                legend_markers.append((cap_outer_circle, cap_inner_circle))
                legend_entries.append(node)

        # Fill the dict with legend kwargs:
        _label_grouped_node_color_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "UID Colorings",
            "legend_bbox_to_anchor": (1.0, 1.0),
            "legend_loc": "upper left",
            "legend_borderaxespad": 0,
        }
        # clear marker and label lists:
        legend_markers = []
        legend_entries = []

        # Energy carrier sorted legend
        for carrier, color in themes.colors.carrier.items():
            if color in self._nformats.node_color.carrier.values():
                node_marker = mpl.lines.Line2D(
                    [],
                    [],
                    marker="o",
                    markerfacecolor=color,
                    markeredgecolor=color,
                    markersize=15,
                    linestyle="",
                )
                legend_markers.append(node_marker)
                legend_entries.append(carrier)

        _carrier_grouped_node_color_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "Energy Carrier Colorings",
            "legend_bbox_to_anchor": (1.0, 0.5),
            "legend_loc": "center left",
            "legend_borderaxespad": 0,
        }

        # wipe marker an label lists:
        legend_markers = []
        legend_entries = []

        # Sector sorted legend
        for sector, color in themes.colors.sector.items():
            if color in self._nformats.node_color.sector.values():
                node_marker = mpl.lines.Line2D(
                    [],
                    [],
                    marker="o",
                    markerfacecolor=color,
                    markeredgecolor=color,
                    markersize=15,
                    linestyle="",
                )
                legend_markers.append(node_marker)
                legend_entries.append(sector)

        _sector_grouped_node_color_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "Sector Colorings",
            "legend_bbox_to_anchor": (1.0, 0.5),
            "legend_loc": "center left",
            "legend_borderaxespad": 0,
        }

        return nts.NodeColorGroupings(
            component=_component_grouped_node_color_legend,
            name=_label_grouped_node_color_legend,
            carrier=_carrier_grouped_node_color_legend,
            sector=_sector_grouped_node_color_legend,
        )

    def _create_node_style_legend(self):
        """
        Create a dict with matplotlib.pyplot.legend kwargs showing node styles

        This is designed for visualizing fency node design aka:

            - variable node size being outer fading circles
            - capacity factors being proportional to cycle filling
            - installed capacities being proportional to outer diameter

        """
        # Create empty marker and label lists:
        legend_markers = list()
        legend_entries = list()

        # Variable node size entries:
        most_outer_circle = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="black",
            alpha=0.3,
            markeredgecolor="black",
            markersize=15,
            linestyle="",
        )

        outer_circle = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="black",
            alpha=0.6,
            markeredgecolor="black",
            markersize=10,
            linestyle="",
        )

        inner_circle = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="black",
            markeredgecolor="black",
            markersize=5,
            linestyle="",
        )

        legend_markers.append((most_outer_circle, outer_circle, inner_circle))
        legend_entries.append("Variable Node Size")

        # Capacity factor entries:
        cap_inner_circle = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="black",
            markeredgecolor="black",
            markersize=10,
            linestyle="",
        )

        cap_outer_circle = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="white",
            markeredgecolor="black",
            markersize=15,
            linestyle="",
        )

        legend_markers.append((cap_outer_circle, cap_inner_circle))
        legend_entries.append(r"Filling $\propto$ Capacity Factor")

        # Installed capacity entries:
        node_size = mpl.lines.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="black",
            markeredgecolor="black",
            markersize=5,
            linestyle="",
        )

        legend_markers.append(node_size)
        legend_entries.append(r"Size $\propto$ Installed Capacity")

        # Fill the dict with legend kwargs:
        _node_style_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "Node Styles",
            "legend_bbox_to_anchor": (1.0, 1),
            "legend_loc": "upper left",
            "legend_borderaxespad": 0,
        }

        return _node_style_legend

    def _create_edge_style_legend(self):
        """
        Create a dict with matplotlib.pyplot.legend kwargs showing edge styles

        This is designed for visualizing fency edge design aka:

            - net energy flow being proportional to edge width
            - specific_emissions being proportional to darkness
            - specific flow costs being proportional to edge length

        """
        # Create empty marker and label lists to be filled in the process
        legend_markers = list()
        legend_entries = list()

        # Length entry:
        arrow_length = mpl.lines.Line2D(
            [], [], marker="$\u279d$", markersize=15, color="black", linestyle=""
        )
        legend_markers.append(arrow_length)
        legend_entries.append(r"Length $\propto$ Flow Costs")

        # Width entry
        arrow_width = mpl.lines.Line2D(
            [],
            [],
            marker="$\u27A7$",
            markersize=15,
            markerfacecolor="black",
            markeredgewidth=0,
            markeredgecolor="black",
            linestyle="",
        )
        legend_markers.append(arrow_width)
        legend_entries.append(r"Width $\propto$ Net Energy Flow")

        # Greyscale entry
        arrow_filling = mpl.lines.Line2D(
            [],
            [],
            marker="$\u27a1$",
            markersize=15,
            markerfacecolor="grey",
            markeredgecolor="grey",
            linestyle="",
        )

        legend_markers.append(arrow_filling)
        legend_entries.append(r"Grey Scale $\propto$ Emissions")

        # Fill the dict with legend kwargs:
        _edge_style_legend = {
            "legend_handles": legend_markers,
            "legend_labels": legend_entries,
            "legend_labelspacing": 1,
            "legend_title": "Energy System Flows",
            "legend_bbox_to_anchor": (1.0, 0),
            "legend_loc": "upper left",
            "legend_borderaxespad": 0,
        }

        return _edge_style_legend


class NodeFormatier(Resultier):
    r"""Transforming energy system results into node visuals.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.

    cgrp: str, default='name'
        Which group of color attribute(s) to return. One of::

            {'name', 'carrier', 'sector'}

        Color related attributes are grouped by
        :class:`tessif.frused.namedtuples.NodeColorGroupings` and are thus
        returned as a :class:`typing.NamedTuple`. Certain api functionalities
        expect those attributes to be dicts. (Usually those working only
        on :class:`~tessif.transform.es2mapping.base.ESTransformer` input).
        Use this parameter on Formatier creation to provide the expected
        dictionary.

    drawutil: str, default='nx'
        Which drawuing utility backend to format node size, fil_size and
        shape to. ``'dc'`` for :mod:`plotly-dash-cytoscape
        <tessif.visualize.dcgrph>` or ``'nx'`` for
        :mod:`networkx-matplotlib <tessif.visualize.nxgrph>`.
    """

    def __init__(self, optimized_es, cgrp="name", drawutil="nx", **kwargs):
        super().__init__(optimized_es=optimized_es, **kwargs)

        self._cgrp = cgrp

        if drawutil not in ["dc", "nx"]:
            logger.warning(
                "Tried to access nonexistent field {} from {}.".format(
                    drawutil, __name__
                )
            )
            logger.warning("Use one of the existing fields: {}".format("['dc', 'nx']"))
            logger.warning("Using default drawing utility: 'dc'")
            self._drawutil = "dc"
        else:
            self._drawutil = drawutil

        if self._drawutil == "nx":
            # mappings for networkx
            self._default_node_shapes = defaults.nxgrph_node_shapes
            self._node_shape = self._map_nx_node_shapes()
            self._node_size = self._map_nx_node_sizes()

        # mappings for dash cytoscape
        if self._drawutil == "dc":
            self._default_node_shapes = defaults.dcgrph_node_shapes
            self._node_shape = self._map_dc_node_shapes()
            self._node_size = self._map_dc_node_sizes()

        self._node_fill_size = self._map_node_fill_size()
        self._node_color = self._map_node_colors()
        self._node_color_maps = self._map_node_color_maps()

    @property
    def node_shape(self):
        r"""Nodes shapes mapped to their respective
        :ref:`node uid representation <Labeling_Concept>`.

        .. csv-table::
            :file: ../../../../docs/source/api/frused/defaults/node_shapes.csv
        """
        return self._node_shape

    @property
    def node_size(self):
        r"""Scaled node sizes mapped to their respective
        :ref:`node uid representation <Labeling_Concept>`.

        Scaled by:

            :math:`\frac{\text{installed capacity}}{\text{reference capacity}}
            \ \cdot` ``self.defaults['node_size']``.

        Nodes of variable size will be set to default size.
        :attr:`installed capacity <CapacityResultier.node_installed_capacity>`
        and
        :attr:`reference capacity <CapacityResultier.node_reference_capacity>`
        are evaluated using :class:`CapacityResultier` on
        :paramref:`~NodeFormatier.optimized_es`.
        """
        return self._node_size

    @property
    def node_fill_size(self):
        r"""Scaled node sizes mapped to their respective
        :ref:`node uid representation <Labeling_Concept>`.

        Scaled using:

            :math:`\text{capacity factor} \ \cdot`
            ``self.defaults['node_size']``

        Nodes fillings of variably sized nodes will be set to default size.
        :attr:`installed capacity
        <CapacityResultier.node_characteristic_value>` is evaluated using
        :class:`CapacityResultier` on :paramref:`~NodeFormatier.optimized_es`.
        """
        return self._node_fill_size

    @property
    def node_color(self):
        """Grouped node colors mapped to their respective
        :ref:`node uid representation <Labeling_Concept>`.

        Grouping utilizes
        :attr:`~tessif.frused.namedtuples.NodeColorGroupings`.
        Available groupings are:

            - :paramref:`~tessif.frused.nametuples.NodeColorGroupings.label`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.carrier`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.sector`

        Return
        ------
        node_colors: tuple, dict
            Depending on :paramref:`~NodeFormatier.cgrp` either all groupings
            are returned as a :class:`typing.NamedTuple` or a single grouping
            as :class:`dictionary <collections.abc.Mapping>`.
        """
        grp = self._cgrp
        if grp == "all":
            return self._node_color
        elif grp in self._node_color._fields:
            return getattr(self._node_color, grp)
        else:
            logger.warning(f"Tried to access nonexistent field {grp} from {__name__}.")
            logger.warning(
                "Use 'all' or one of the existing fields: {}".format(
                    nts.NodeColorGroupings._fields
                )
            )
            logger.warning("Returning default group")
            return self._node_color.label

    @property
    def node_color_maps(self):
        r"""Same as :attr:`node_color` with
        :attr:`color maps <tessif.frused.themes.cmaps>` that are cycled through
        for each member of the group.

        Return
        ------
        node_color_maps: tuple, dict
            Depending on :paramref:`~NodeFormatier.cgrp` either all groupings
            are returned as a :class:`typing.NamedTuple` or a single grouping
            as :class:`dictionary <collections.abc.Mapping>`.
        """
        grp = self._cgrp
        if grp == "all":
            return self._node_color_maps
        elif grp in self._node_color_maps._fields:
            return getattr(self._node_color_maps, grp)
        else:
            logger.warning(f"Tried to access nonexistent field {grp} from {__name__}.")
            logger.warning(
                "Use 'all' or one of the existing fields: {}".format(
                    nts.NodeColorGroupings._fields
                )
            )
            logger.warning("Returning default group")
            return self._node_color_maps.label

    def _map_nx_node_shapes(self):
        """Interface to map the :ref:`model <SupportedModels>` specific,
        optimized energy system component :ref:`uid representations
        <Labeling_Concept>` to a node shape specifying string.
        """
        # Use a defaultdict as node shape container:
        _nx_node_shape = defaultdict(str)

        component_types = ["bus", "connector", "sink", "storage", "transformer"]

        for node in self.nodes:
            # Singular mapped component types

            if self.uid_nodes[node].component.lower() in component_types:
                for component_type in component_types:

                    if self.uid_nodes[node].component in getattr(
                        spellings, component_type
                    ):
                        _nx_node_shape[node] = defaults.nxgrph_node_shapes.get(
                            component_type
                        )

            # Source
            elif self.uid_nodes[node].component in spellings.source:
                # set source to default shape...
                _nx_node_shape[node] = self._default_node_shapes.get("default_source")

                # ... unless its a pv source
                if any(expr in node for expr in esci.name["photovoltaic"]):
                    _nx_node_shape[node] = self._default_node_shapes.get("solar")

                # ... unless its a wind onshore source
                if any(expr in node for expr in esci.name["onshore"]):
                    _nx_node_shape[node] = self._default_node_shapes.get("wind")

                # ... unless its a wind offshore source
                if any(expr in node for expr in esci.name["offshore"]):
                    _nx_node_shape[node] = self._default_node_shapes.get("wind")

                # ... unless its a commodity_source
                if any(
                    expr in node
                    for source in ["gas", "oil", "lignite", "hardcoal", "nuclear"]
                    for expr in esci.carrier[source]
                ):
                    _nx_node_shape[node] = self._default_node_shapes.get(
                        "commodity_source"
                    )
            else:
                msg = (
                    f"Uid component '({self.uid_nodes[node].component})' "
                    + "was not recognized. Registered component types are "
                    + f"'{component_types}' and 'source'."
                )
                raise TypeError(msg)

        return dict(_nx_node_shape)

    def _map_dc_node_shapes(self):
        """Interface to map the :ref:`model <SupportedModels>` specific,
        optimized energy system component :ref:`uid representations
        <Labeling_Concept>` to a node shape specifying string.
        """
        # Use a defaultdict as node shape container:
        _dc_node_shape = defaultdict(str)

        component_types = ["bus", "connector", "sink", "storage", "transformer"]

        for node in self.nodes:
            # Singular mapped component types

            if self.uid_nodes[node].component.lower() in component_types:
                for component_type in component_types:

                    if self.uid_nodes[node].component in getattr(
                        spellings, component_type
                    ):
                        _dc_node_shape[node] = defaults.dcgrph_node_shapes.get(
                            component_type
                        )

            # Source
            elif self.uid_nodes[node].component in spellings.source:
                # set source to default shape...
                _dc_node_shape[node] = self._default_node_shapes.get("default_source")

                # ... unless its a pv source
                if any(expr in node for expr in esci.name["photovoltaic"]):
                    _dc_node_shape[node] = self._default_node_shapes.get("solar")

                # ... unless its a wind onshore source
                if any(expr in node for expr in esci.name["onshore"]):
                    _dc_node_shape[node] = self._default_node_shapes.get("wind")

                # ... unless its a wind offshore source
                if any(expr in node for expr in esci.name["offshore"]):
                    _dc_node_shape[node] = self._default_node_shapes.get("wind")

                # ... unless its a commodity_source
                if any(
                    expr in node
                    for source in ["gas", "oil", "lignite", "hardcoal", "nuclear"]
                    for expr in esci.carrier[source]
                ):
                    _dc_node_shape[node] = self._default_node_shapes.get(
                        "commodity_source"
                    )
            else:
                msg = (
                    f"Uid component '({self.uid_nodes[node].component})' "
                    + "was not recognized. Registered component types are "
                    + f"'{component_types}' and 'source'."
                )
                raise TypeError(msg)

        return dict(_dc_node_shape)

    def _map_nx_node_sizes(self):
        r"""Interface to map and scale node sizes of the :ref:`model
        <SupportedModels>` specific, optimized energy system components to
        their respective :ref:`uid representation <Labeling_Concept>`.

        Node are scaled using:

            :math:`\frac{\text{installed capacity}}{\text{reference capacity}}
            \ \cdot` ``self.defaults['node_size']``.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.NodeFormatier` source code for exemplary
        implementation.
        """
        # Use a defaultdict as node shape container:
        _node_size = defaultdict(int)

        # Map the node sizes:
        for node in self.nodes:
            # if self.uid_nodes[node] in spellings.bus:
            #     _node_size[node] = 'variable'
            # else:
            inst_cap = self.node_installed_capacity[node]

            if isinstance(inst_cap, collections.abc.Iterable):
                # use the maximum of the installed capacities in case
                # of ambiguous installed capacities
                inst_cap = max(inst_cap.fillna(-1))
                if inst_cap == -1:
                    _node_size[node] = "variable"

            # is node of variable size ?
            if inst_cap == defaults.energy_system_nodes["variable_capacity"]:
                # yes, so set variable
                _node_size[node] = "variable"
            else:
                # no, so scale node size:
                _node_size[node] = round(
                    inst_cap
                    / self.node_reference_capacity
                    * defaults.nxgrph_visualize_defaults["node_size"]
                )

                # cap minimum node size:
                _node_size[node] = max(
                    _node_size[node],
                    defaults.nxgrph_visualize_defaults["node_minimum_size"],
                )

        return dict(_node_size)

    def _map_dc_node_sizes(self):
        r"""Interface to map and scale node sizes of the :ref:`model
        <SupportedModels>` specific, optimized energy system components to
        their respective :ref:`uid representation <Labeling_Concept>`.

        Node are scaled using:

            :math:`\frac{\text{installed capacity}}{\text{reference capacity}}
            \ \cdot` ``self.defaults['node_size']``.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.NodeFormatier` source code for exemplary
        implementation.
        """
        # Use a defaultdict as node shape container:
        _dc_node_size = defaultdict(int)

        # Map the node sizes:
        for node in self.nodes:
            # if self.uid_nodes[node] in spellings.bus:
            #     _dc_node_size[node] = 'variable'
            # else:
            inst_cap = self.node_installed_capacity[node]

            if isinstance(inst_cap, collections.abc.Iterable):
                # use the maximum of the installed capacities in case
                # of ambiguous installed capacities
                inst_cap = max(inst_cap.fillna(-1))
                if inst_cap == -1:
                    _dc_node_size[node] = "variable"

            # is node of variable size ?
            if inst_cap == defaults.energy_system_nodes["variable_capacity"]:
                # yes, so set variable
                _dc_node_size[node] = "variable"
            else:
                # no, so scale node size:
                _dc_node_size[node] = round(
                    inst_cap
                    / self.node_reference_capacity
                    * defaults.dcgrph_visualize_defaults["node_size"]
                )

                # cap minimum node size:
                _dc_node_size[node] = max(
                    _dc_node_size[node],
                    defaults.dcgrph_visualize_defaults["node_minimum_size"],
                )

        return dict(_dc_node_size)

    def _map_node_fill_size(self):
        r"""Interface to map and scale node fill sizes of the :ref:`model
        <SupportedModels>` specific, optimized energy system components to
        their respective :ref:`uid representation <Labeling_Concept>`.

        Fill size is scaled using:

            :math:`\text{capacity factor} \ \cdot`
            ``self.defaults['node_size']``.

        Note
        ----
        Needs to be overridden by the model specific child class!

        Check :class:`es2mapping.omf.NodeFormatier` source code for exemplary
        implementation.
        """
        # Use a defaultdict as node shape container:
        _node_fill_size = defaultdict(float)

        for node in self.nodes:
            # is node size variable ?
            if self.node_size[node] == "variable":
                # yes, so set filling to None
                _node_fill_size[node] = None
            else:
                # no, so scale it using cf*default_size
                cv = self.node_characteristic_value[node]
                if isinstance(cv, collections.abc.Iterable):
                    cv = min(cv)

                fill_size = round(self.node_size[node] * cv, 0)
                if np.isnan(fill_size):
                    fill_size = 0.0
                _node_fill_size[node] = fill_size

        return dict(_node_fill_size)

    def _map_node_colors(self):
        """Interface to map node colors of the :ref:`model
        <SupportedModels>` specific, optimized energy system components to
        their respective :ref:`uid representation <Labeling_Concept>`.
        """

        # Use a defaultdict as node color container:
        _component_grouped_node_colors = defaultdict(str)
        _name_grouped_node_colors = defaultdict(str)
        _carrier_grouped_node_colors = defaultdict(str)
        _sector_grouped_node_colors = defaultdict(str)

        # Map the node colors:
        for node in self.nodes:

            # component identifier grouped node colors
            for key, variations in esci.component.items():
                if hasattr(self.uid_nodes[node], "component") and any(
                    tag == self.uid_nodes[node].component for tag in variations
                ):
                    _component_grouped_node_colors[node] = themes.colors.component[key]

            # name grouped node colors
            for key, variations in esci.name.items():
                if any(tag == self.uid_nodes[node].name for tag in variations):
                    _name_grouped_node_colors[node] = themes.colors.name[key]

            # carrier grouped node colors
            for key, variations in esci.carrier.items():
                if hasattr(self.uid_nodes[node], "carrier") and any(
                    tag == self.uid_nodes[node].carrier for tag in variations
                ):
                    _carrier_grouped_node_colors[node] = themes.colors.carrier[key]

            # sector grouped node colors
            for key, variations in esci.sector.items():
                if hasattr(self.uid_nodes[node], "sector") and any(
                    tag == self.uid_nodes[node].sector for tag in variations
                ):
                    _sector_grouped_node_colors[node] = themes.colors.sector[key]

        # Fill all previously uncolored nodes with default color...
        for node in self.nodes:

            # ... except for name grouped nodes, which are tried to be filled
            # with tag->color for tags being subtags of themes.color.keys()
            if not _name_grouped_node_colors[node]:
                for category in esci._asdict().keys():
                    for key, variations in esci._asdict()[category].items():

                        if any(tag in node for tag in variations):
                            _name_grouped_node_colors[node] = getattr(
                                themes.colors, category
                            ).get(key, defaults.nxgrph_visualize_defaults["node_color"])

            # Component grouped nodes
            if not _component_grouped_node_colors[node]:
                _component_grouped_node_colors[
                    node
                ] = defaults.nxgrph_visualize_defaults["node_color"]

            if not _name_grouped_node_colors[node]:
                _name_grouped_node_colors[node] = defaults.nxgrph_visualize_defaults[
                    "node_color"
                ]

            # Carrier grouped nodes
            if not _carrier_grouped_node_colors[node]:
                _carrier_grouped_node_colors[node] = defaults.nxgrph_visualize_defaults[
                    "node_color"
                ]

            # Sector grouped nodes
            if not _sector_grouped_node_colors[node]:
                _sector_grouped_node_colors[node] = defaults.nxgrph_visualize_defaults[
                    "node_color"
                ]

        return nts.NodeColorGroupings(
            component=dict(_component_grouped_node_colors),
            name=dict(_name_grouped_node_colors),
            carrier=dict(_carrier_grouped_node_colors),
            sector=dict(_sector_grouped_node_colors),
        )

    def _map_node_color_maps(self):
        """Interface to map node colors of the :ref:`model
        <SupportedModels>` specific, optimized energy system components to
        their respective :ref:`uid representation <Labeling_Concept>`.
        """

        # Use a defaultdict as node color container:
        _component_grouped_node_color_maps = defaultdict(str)
        _name_grouped_node_color_maps = defaultdict(str)
        _carrier_grouped_node_color_maps = defaultdict(str)
        _sector_grouped_node_color_maps = defaultdict(str)

        # Map the node color maps:
        for node in self.nodes:
            # component grouped node color maps
            for key, variations in esci.component.items():
                if hasattr(self.uid_nodes[node], "component") and any(
                    tag == self.uid_nodes[node].component for tag in variations
                ):
                    _component_grouped_node_color_maps[node] = next(
                        themes.ccycles.component[key]
                    )

            # name grouped node color maps
            for key, variations in esci.name.items():

                # name grouped node color maps
                if any(tag == self.uid_nodes[node].name for tag in variations):
                    _name_grouped_node_color_maps[node] = next(themes.ccycles.name[key])

            # carrier grouped node color maps
            for key, variations in esci.carrier.items():
                if hasattr(self.uid_nodes[node], "carrier") and any(
                    tag == self.uid_nodes[node].carrier for tag in variations
                ):
                    _carrier_grouped_node_color_maps[node] = next(
                        themes.ccycles.carrier[key]
                    )

                # sector grouped node color maps
            for key, variations in esci.sector.items():
                if hasattr(self.uid_nodes[node], "sector") and any(
                    tag == self.uid_nodes[node].sector for tag in variations
                ):
                    _sector_grouped_node_color_maps[node] = next(
                        themes.ccycles.sector[key]
                    )

        # Fill all previously uncolored nodes with default color...
        for node in self.nodes:

            # Component grouped nodes
            if not _component_grouped_node_color_maps[node]:
                _component_grouped_node_color_maps[
                    node
                ] = defaults.nxgrph_visualize_defaults["node_color"]

            # ... except for name grouped nodes, which are tried to be filled
            # with tag->color for tags being subtags of colormaps.keys()
            if not _name_grouped_node_color_maps[node]:
                for category in esci._asdict().keys():
                    for key, variations in esci._asdict()[category].items():

                        if any(tag in node for tag in variations):
                            _name_grouped_node_color_maps[node] = next(
                                getattr(themes.ccycles, category).get(
                                    key,
                                    cycle(
                                        defaults.nxgrph_visualize_defaults[
                                            "node_color_map"
                                        ]
                                    ),
                                )
                            )

            if not _name_grouped_node_color_maps[node]:
                _name_grouped_node_color_maps[
                    node
                ] = defaults.nxgrph_visualize_defaults["node_color"]

            # Carrier grouped nodes
            if not _carrier_grouped_node_color_maps[node]:
                _carrier_grouped_node_color_maps[
                    node
                ] = defaults.nxgrph_visualize_defaults["node_color"]

            # Sector grouped nodes
            if not _sector_grouped_node_color_maps[node]:
                _sector_grouped_node_color_maps[
                    node
                ] = defaults.nxgrph_visualize_defaults["node_color"]

        # Return the mappings:
        return nts.NodeColorGroupings(
            component=dict(_component_grouped_node_color_maps),
            name=dict(_name_grouped_node_color_maps),
            carrier=dict(_carrier_grouped_node_color_maps),
            sector=dict(_sector_grouped_node_color_maps),
        )


class EdgeFormatier(Resultier):
    r"""Transforming energy system results into edge visuals.

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.
    drawutil: str, default='nx'
        Which drawuing utility backend to format node size, fil_size and
        shape to. ``'dc'`` for :mod:`plotly-dash-cytoscape
        <tessif.visualize.dcgrph>` or ``'nx'`` for
        :mod:`networkx-matplotlib <tessif.visualize.nxgrph>`.
    cls: tuple, default=None
        2-Tuple / :attr:`CLS namedtuple <tessif.frused.namedtuples.CLS>`
        defining the relative flow cost thresholds and the respective style
        specifications. Used to map specific flow costs to edge line style
        representations.

        If  ``None``, default implementation is used based on
        :paramref:`~EdgeFormatier.drawutil`.

        For ``drawutil='nx'``
        `Networkx-Matplotlib
        <https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Patch.html#matplotlib.patches.Patch.set_linestyle>`_::

            cls = ([0, .33, .66], ['dotted', 'dashed', 'solid'])

        For ``drawutil='dc'``
        `Dash-Cytoscape <https://js.cytoscape.org/#style/edge-line>`_ styles
        are used::

            cls = ([0, .33, .66], ['dotted', 'dashed', 'solid'])

        Translating to all edges of relative specific flows costs, between
        ``0`` and ``.33`` are correlated to have a ``':'``/``'dotted'``
        linestyle.
    """

    def __init__(self, optimized_es, drawutil="nx", cls=None, **kwargs):

        super().__init__(optimized_es=optimized_es, **kwargs)

        # parse drawutil arg
        if drawutil not in ["dc", "nx"]:
            logger.warning(
                "Tried to access nonexistent field {} from {}.".format(
                    drawutil, __name__
                )
            )
            logger.warning("Use one of the existing fields: {}".format("['dc', 'nx']"))
            logger.warning("Using default drawing utility: 'dc'")
            self._drawutil = "dc"
        else:
            self._drawutil = drawutil

        # broaden edges based on drawutil:
        if self._drawutil == "nx":
            self._edge_width = self._map_nx_edge_width()
            self._edge_color = self._map_nx_edge_colors()

            _cls = ([0, 0.33, 0.66], [":", "--", "-"])
            # style translates to ['dotted', 'dashed', 'solid']

        # mappings for dash cytoscape
        if self._drawutil == "dc":
            self._edge_width = self._map_dc_edge_width()
            self._edge_color = self._map_dc_edge_colors()
            _cls = ([0, 0.33, 0.66], ["dotted", "dashed", "solid"])

        if not cls:
            self._cls = nts.CLS(*_cls)

        self._edge_linestyle = self._map_edge_linestyles()

    @property
    def edge_width(self):
        """Edge widths mapped to their respective Edges.

        Widths are scaled with the edge's energy flow. The bigger the flow, the
        wider the edge.

        Returns
        -------
        edge_width: dict
            Dictionairies of edge widths (numbers) mapped to their respective
            :class:`Edges <tessif.frused.namedtuples.Edge>`.
        """
        return self._edge_width

    @property
    def edge_color(self):
        """Edge colors mapped to their respective Edge.

        Greyscale is scaled with emissions. The less gray, the less emissions.

        Returns
        -------
        edge_color: dict
            Dictionairies of greyscale (numbers between ``0.0`` and ``1.0``)
            mapped to their respective
            :class:`Edges <tessif.frused.namedtuples.Edge>`.
        """
        return self._edge_color

    @property
    def edge_linestyle(self):
        """Edge line style mapped to their respective Edge.

        Styles correlated specific ``flow_costs`` to thresholds as defined
        during instance ceation. The less expansive, the less solid the line
        style.

        Returns
        -------
        edge_linestyle: dict
            Dictionairies of linestyles (string specifiers like ``'dashed'``
            and ``'dotted'``) mapped to their respective
            :class:`Edges <tessif.frused.namedtuples.Edge>`.
        """
        return self._edge_linestyle

    def _map_nx_edge_width(self):
        """
        Interface for mapping the edge widths to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`. Widths are scaled with
        their net energy flows, the bigger the flow, the wider the edge
        """
        # Use default dict as edge width container using global default:
        _edge_width = defaultdict(
            lambda: defaults.nxgrph_visualize_defaults["edge_width"]
        )

        # Map the respective edge width:
        for edge in self.edges:
            _edge_width[edge] = round(
                self.edge_net_energy_flow[edge]
                / self.edge_reference_net_energy_flow
                * defaults.nxgrph_visualize_defaults["edge_width"],
                2,
            )

            if (
                _edge_width[edge]
                < defaults.nxgrph_visualize_defaults["edge_minimum_width"]
            ):
                _edge_width[edge] = defaults.nxgrph_visualize_defaults[
                    "edge_minimum_width"
                ]

        return dict(_edge_width)

    def _map_dc_edge_width(self):
        """
        Interface for mapping the edge widths to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`. Widths are scaled with
        their net energy flows, the bigger the flow, the wider the edge
        """
        # Use default dict as edge width container using global default:
        _edge_width_cyt = defaultdict(
            lambda: defaults.dcgrph_visualize_defaults["edge_width"]
        )

        # Map the respective edge width:
        for edge in self.edges:
            _edge_width_cyt[edge] = round(
                self.edge_net_energy_flow[edge]
                / self.edge_reference_net_energy_flow
                * defaults.dcgrph_visualize_defaults["edge_width"],
                2,
            )

            # make sure edge with is greater min
            _edge_width_cyt[edge] = max(
                _edge_width_cyt[edge],
                defaults.dcgrph_visualize_defaults["edge_minimum_width"],
            )

        return dict(_edge_width_cyt)

    def _map_nx_edge_colors(self):
        """Interface for mapping edge colors to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`.

        Greyscale is scaled with emissions. The less gray, the less emissions.
        """
        # List as defaultdict entry is used, cause draw_networkx_edges expects
        # iterable of floats when using a colormap
        _edge_colors = defaultdict(list)

        for edge in self.edges:
            edge_color = round(
                self.edge_specific_emissions[edge] / self.edge_reference_emissions, 2
            )

            if edge_color < defaults.nxgrph_visualize_defaults["edge_minimum_grey"]:
                edge_color = defaults.nxgrph_visualize_defaults["edge_minimum_grey"]

            _edge_colors[edge].append(edge_color)

        return dict(_edge_colors)

    def _map_dc_edge_colors(self):
        """Interface for mapping edge colors to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`.

        Greyscale is scaled with emissions. The less gray, the less emissions.
        """
        # List as defaultdict entry is used, cause draw_networkx_edges expects
        # iterable of floats when using a colormap
        _edge_colors = defaultdict(
            lambda: dcgrph_visualize_defaults["edge_minimum_grey"]
        )

        for edge in self.edges:
            # scale color to emission/max_emissions
            edge_color_float = round(
                self.edge_specific_emissions[edge] / self.edge_reference_emissions, 2
            )
            # cap lower end of scale
            edge_color_float = max(
                edge_color_float,
                defaults.dcgrph_visualize_defaults["edge_minimum_grey"],
            )

            # convert float in [0.0, 1.0] to hexcolor value
            _edge_colors[edge] = utils.greyscale2hex(edge_color_float)

        return dict(_edge_colors)

    def _map_edge_linestyles(self):
        """Interface for mapping edge colors to their respective :class:`Edges
        <tessif.frused.namedtuples.Edge>`. Greyscale is scaled
        with emissions. The less gray, the less emissions."""

        # List as defaultdict entry is used, cause draw_networkx_edges expects
        # iterable of floats when using a colormap
        _edge_linestyles = defaultdict(
            lambda: dcgrph_visualize_defaults["edge_linestyle"]
        )

        # scale color relative to max emissions
        max_costs = max(self.edge_specific_flow_costs.values())
        # avoid division by zero
        if max_costs == 0:
            max_costs = 1

        for edge in self.edges:
            # scale color to emission/max_emissions
            edge_cost_float = self.edge_specific_flow_costs[edge] / max_costs

            # correlate linestyles according to thresholds
            for pos, threshold in enumerate(self._cls.thresholds):
                if edge_cost_float >= threshold:
                    _edge_linestyles[edge] = self._cls.styles[pos]

            # enforce default in case something wierd happens:
            if edge not in _edge_linestyles:
                _edge_linestyles[edge] = dcgrph_visualize_defaults["edge_linestyle"]
        return dict(_edge_linestyles)


class ICRHybridier(Resultier):
    """
    Aggregate numerical and visual information for visualizing
    the :ref:`Integrated_Component_Results` (ICR).

    Parameters
    ----------
    optimized_es:
        :ref:`Model <SupportedModels>` specific, optimized energy system
        containing its results.
    """

    def __init__(
        self,
        optimized_es,
        node_formatier,
        edge_formatier,
        mpl_legend_formatier,
        **kwargs,
    ):

        super().__init__(optimized_es=optimized_es, **kwargs)

        # needed resultiers
        self._edge_formatier = edge_formatier
        self._node_formatier = node_formatier
        self._mpl_legend_formatier = mpl_legend_formatier

    @property
    def edge_color(self):
        r"""Edge colors mapped to their Edge names.

        The **edge greyscale** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **specific emissions**.
        """
        return self._edge_formatier.edge_color

    @property
    def edge_len(self):
        r"""
        Edge length mapped to their Edge names.

        The **edge length** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **specific flow costs**.
        """
        return self._edge_formatier.edge_len

    @property
    def edge_weight(self):
        r"""
        Edge length mapped to their Edge names.

        The **edge length** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **specific flow costs**.
        """
        return self._edge_formatier.edge_weight

    @property
    def edge_net_energy_flow(self):
        r"""
        Return sum of time series flow results mapped to
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`\sum\limits_{t} \text{flow}\left(Edge\right)`

        The **edge width** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **net energy flow**.
        """
        return self._edge_formatier.edge_net_energy_flow

    @property
    def edge_specific_flow_costs(self):
        r"""
        Return energy specific flow costs mapped to
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`c_{\text{flow}}` in
        :math:`\frac{\text{cost unit}}{\text{energy unit}}`

        The **edge length** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **specific flow costs**.
        """

        return self._edge_formatier.edge_specific_flow_costs

    @property
    def edge_specific_emissions(self):
        r"""
        Return energy specific emissions mapped to
        :class:`Edges <tessif.frused.namedtuples.Edge>`.

        :math:`e_{\text{flow}}` in
        :math:`\frac{\text{emission unit}}{\text{energy unit}}`

        The **edge greyscale** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **specific emissions**.
        """

        return self._edge_formatier.edge_specific_emissions

    @property
    def edge_width(self):
        r"""
        Edge widths mapped to their Edge names.

        The **edge width** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **net energy flow**.
        """
        return self._edge_formatier.edge_width

    @property
    def node_characteristic_value(self):
        r"""Characteristic values of the energy system components mapped to
        their :ref:`node uid representation <Labeling_Concept>`.

        Components of variable size or have a characteristic value as stated in
        :attr:`tessif.frused.defaults.energy_system_nodes`.

        Characteristic value in this context means:

            - :math:`cv = \frac{\text{characteristic flow}}
              {\text{installed capacity}}` for:

                - :class:`~tessif.model.components.Connector` objects
                - :class:`~tessif.model.components.Source` objects
                - :class:`~tessif.model.components.Sink` objects
                - :class:`~tessif.model.components.Transformer` objects

            - :math:`cv = \frac{\text{mean}\left(\text{SOC}\right)}
              {\text{capacity}}` for:

                - :class:`~tessif.model.components.Storage`


        Characteristic flow in this context means:

            - ``mean(`` :attr:`LoadResultier.node_summed_loads` ``)``

                - :class:`~tessif.model.components.Source` objects
                - :class:`~tessif.model.components.Sink` objects

            - ``mean(0th outflow)`` for:

                - :class:`~tessif.model.components.Transformer` objects

        The **node fillsize** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **characteristic value**.
        If no capacity is defined (i.e for nodes of variable size, like busses
        or excess sources and sinks, node size is set to it's default (
        :attr:`nxgrph_visualize_defaults[node_fill_size]
        <tessif.frused.defaults.nxgrph_visualize_defaults>`).
        """
        return self._node_formatier.node_characteristic_value

    @property
    def node_color(self):
        """Grouped node colors mapped to their node names.

        Grouping utilizes
        :attr:`~tessif.frused.namedtuples.NodeColorGroupings`.
        Available groupings are:

            - :paramref:`~tessif.frused.nametuples.NodeColorGroupings.label`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.carrier`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.sector`
        """
        return self._node_formatier.node_color

    @property
    def node_installed_capacity(self):
        r"""Return the installed capacities of the energy system components as
        mapping keyed by node label. Components of variable size have an
        installed capacity of None

        :math:`P_{cap}= \text{installed capacity}`

        The **node size** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **installed capacity**.
        If no capacity is defined (i.e for nodes of variable size, like busses
        or excess sources and sinks, node size is set to it's default (
        :attr:`nxgrph_visualize_defaults[node_size]
        <tessif.frused.defaults.nxgrph_visualize_defaults>`).
        """
        return self._node_formatier.node_installed_capacity

    @property
    def node_shape(self):
        r"""Nodes shapes mapped to their node names

        .. csv-table:: Node shape mapping
            :widths: 20, 6, 20, 6

            "'default_source'", "'o'", "'bus'", "'o'"
            "'commodity_source'", "'o'", "'transformer'", "'8'"
            "'solar'", "'s'", "'sink'", "'8'"
            "'wind'", "'h'", "storage", "s"
        """
        return self._node_formatier.node_shape

    @property
    def node_size(self):
        r"""Scaled node sizes mapped to their node names.

        Scaled by:

            :math:`\frac{\text{installed capacity}}{\text{reference capacity}}
            \ \cdot` ``self.defaults['node_size']``.

        :attr:`Installed capacity <ICRHybridier.node_installed_capacity>`
        and
        :attr:`reference capacity <CapacityResultier.node_reference_capacity>`
        are evaluated using :class:`CapacityResultier` on
        :paramref:`~NodeFormatier.optimized_es`.

        The **node size** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the **installed capacity**.
        If no capacity is defined (i.e for nodes of variable size, like busses
        or excess sources and sinks, node size is set to it's default (
        :attr:`nxgrph_visualize_defaults[node_size]
        <tessif.frused.defaults.nxgrph_visualize_defaults>`).
        """
        return self._node_formatier.node_size

    @property
    def node_fill_size(self):
        r"""Scaled node sizes mapped to their node names.

        Scaled using:

            :math:`\text{capacity factor} \ \cdot`
            ``self.defaults['node_size']``

        :attr:`Installed capacity <ICRHybridier.node_characteristic_value>`
        is evaluated using :class:`CapacityResultier` on
        :paramref:`~NodeFormatier.optimized_es`.

        The **node fillsize** of :ref:`integrated component results graphs
        <Integrated_Component_Results>` scales with the
        **characteristic value**.
        If no capacity is defined (i.e for nodes of variable size, like busses
        or excess sources and sinks, node size is set to it's default (
        :attr:`nxgrph_visualize_defaults[node_fill_size]
        <tessif.frused.defaults.nxgrph_visualize_defaults>`).
        """
        return self._node_formatier.node_fill_size

    @property
    def legend_of_nodes(self):
        r"""
        Color grouped matplotlib legend attributes mapped to their parameter.

        Grouping utilizes
        :attr:`~tessif.frused.namedtuples.NodeColorGroupings`.
        Available groupings are:

            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.label`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.carrier`
            - :paramref:`~tessif.frused.namedtuples.NodeColorGroupings.sector`
        """
        return self._mpl_legend_formatier.node_legend

    @property
    def legend_of_node_styles(self):
        """Matplotlib legend attributes mapped to their parameters to describe
        :paramref:`fency node styles
        <tessif.visualize.nxgrph.draw_nodes.draw_fency_nodes>`. Fency as in:

            - variable node size being outer fading circles
            - cycle filling being proportional capacity factors
            - outer diameter being proportional installed capacities

        """
        return self._mpl_legend_formatier.node_style_legend

    @property
    def legend_of_edge_styles(self):
        """Matplotlib legend attributes mapped to their parameters to describe
        the edge style of :ref:`integrated component results graphs
        <Integrated_Component_Results>`. As in:

            - **edge length** scaling with **specific flow costs**
            - **edge width** scaling with **net energy flow**
            - **grey scale** scaling with **speficifc flow emissions**
        """
        return self._mpl_legend_formatier.edge_style_legend
