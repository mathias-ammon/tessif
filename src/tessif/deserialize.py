"""Restore / Deserialize previously serialized tessif features using json."""
import json
from ast import literal_eval
from collections import defaultdict

import pandas as pd

from tessif.frused.namedtuples import Edge, Uid


class RestoredResults:
    """Json Deserialzed Resultiers."""

    def __init__(self, json_stream):
        """Deserialze Resuliter serialized results."""
        for key, value in json_stream.items():
            if key in sm_deserializer.keys():
                setattr(self, key.lstrip("_"), sm_deserializer[key](value))

    _recognized_system_results = [
        "nodes",
        "edges",
        "uid_nodes",
        "inbounds",
        "outbounds",
        "number_of_constraints",
        "reference_net_energy_flow",
        "reference_emissions",
        "reference_capacity",
        "global_results",
    ]

    _recognized_node_results = [
        "states_of_charge",
        "node_loads",
        "inflows",
        "outflows",
        "installed_capacities",
        "original_capacities",
        "characteristic_values",
    ]

    _recognized_edge_results = [
        "net_energy_flows",
        "specific_flow_costs",
        "specific_emissions",
        "edge_weights",
        "edge_len",
        "expansion_costs",
    ]

    @property
    def node_data(self):
        """Return all recognized node keyed results."""
        dct = {
            attr_name: getattr(self, attr_name)
            for attr_name in self._recognized_node_results
            if hasattr(self, attr_name)
        }
        dct = dict(sorted(dct.items()))
        return dct

    @property
    def edge_data(self):
        """Return all recognized edge keyed results."""
        dct = {
            attr_name: getattr(self, attr_name)
            for attr_name in self._recognized_edge_results
            if hasattr(self, attr_name)
        }

        dct = dict(sorted(dct.items()))
        return dct

    @property
    def system_wide_data(self):
        """Return all recognized system wide results."""
        dct = {
            attr_name: getattr(self, attr_name)
            for attr_name in self._recognized_system_results
            if hasattr(self, attr_name)
        }

        dct = dict(sorted(dct.items()))
        return dct

    @property
    def inbounds(self):
        """Inbound node mapping.

        :class:`~collection.abc.Mapping` of a list of inbound nodes
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

        # sort by keys
        _inbounds = dict(sorted(_inbounds.items()))
        # sort by nodes and turn into tuple
        for key in _inbounds.copy().keys():
            _inbounds[key] = tuple(sorted(_inbounds[key]))

        return dict(_inbounds)

    @property
    def outbounds(self):
        """Outbound node mapping.

        :class:`~collection.abc.Mapping` of a list of outbound nodes
        (in fact their uid string representations)
        to the node (in fact its uid string representations) being the source
        of the outbounds.

        Meaning, for an energy system like ``1 <- 2 -> 3``, this mapping would
        look like ::

            outbounds['1'] == []
            outbounds['2'] == ['1', '3']
        """
        _outbounds = defaultdict(list)
        for node in self.nodes:
            for edge in self.edges:
                if node == edge.source:
                    _outbounds[node].append(edge.target)

        # sort by keys
        _outbounds = dict(sorted(_outbounds.items()))
        # sort by nodes and turn into tuple
        for key in _outbounds.copy().keys():
            _outbounds[key] = tuple(sorted(_outbounds[key]))

        return dict(_outbounds)


def deserialize_nodes(nodes):
    """Deserialize node results."""
    return list(sorted(nodes))


def deserialize_uid_nodes(node_uid_dict):
    """Deserialize node uids."""
    nuids = {}
    for value in node_uid_dict.values():
        node_uid = Uid(*value)
        nuids[node_uid.name] = node_uid

    nuids = dict(sorted(nuids.items()))
    return nuids


def deserialize_eges(edge_list):
    """Deserialize edge results."""
    edges = []
    for listed_edge in edge_list:
        edges.append(Edge(*listed_edge))

    return list(sorted(edges))


def deserialize_pure_dict_results(results_dict):
    """Deserialize dict results needing no additional parsing."""
    return dict(sorted(results_dict.items()))


def deserialize_singular_results_values(result_values):
    """Deserialize singular value results."""
    return result_values


def deserialize_dicts_of_pdseries_results(result_dict):
    """Deserialize dicts of pandas series results."""
    results = {}
    for key, value in sorted(result_dict.items()):
        results[key] = pd.read_json(value, orient="split", typ="series")
    return results


def deserialize_dicts_of_dataframe_results(results_dict):
    """Deserialize number of constraints results."""
    results = {}
    for key, value in sorted(results_dict.items()):
        results[key] = pd.read_json(value, orient="split", typ="frame")
    return results


def deserialize_edge_keyed_results(results_dict):
    """Deserialize net energy flow results."""
    edge_keyed_results = {}

    # remove stringified container strings
    remove_chars = "[]() "

    # create a translation table that maps each character to None
    translation_table = str.maketrans("", "", remove_chars)

    for key, value in sorted(results_dict.items()):
        # remove the container string characters using the translation table
        destringified_edge = key.translate(translation_table)

        # split the edge string in source and target and create the edge
        edge = Edge(*destringified_edge.split(","))
        edge_keyed_results[edge] = value

    return edge_keyed_results


sm_deserializer = {
    "_nodes": deserialize_nodes,
    "_uid_nodes": deserialize_uid_nodes,
    "_edges": deserialize_eges,
    "_global_results": deserialize_pure_dict_results,
    "_number_of_constraints": deserialize_singular_results_values,
    "_states_of_charge": deserialize_dicts_of_pdseries_results,
    "_node_loads": deserialize_dicts_of_dataframe_results,
    "_inflows": deserialize_dicts_of_dataframe_results,
    "_outflows": deserialize_dicts_of_dataframe_results,
    "_net_energy_flows": deserialize_edge_keyed_results,
    "_specific_flow_costs": deserialize_edge_keyed_results,
    "_specific_emissions": deserialize_edge_keyed_results,
    "_edge_weights": deserialize_edge_keyed_results,
    "_edge_len": deserialize_edge_keyed_results,
    "_reference_net_energy_flow": deserialize_singular_results_values,
    "_reference_emissions": deserialize_singular_results_values,
    "_reference_capacity": deserialize_singular_results_values,
    "_installed_capacities": deserialize_pure_dict_results,
    "_original_capacities": deserialize_pure_dict_results,
    "_characteristic_values": deserialize_pure_dict_results,
    "_expansion_costs": deserialize_pure_dict_results,
}


class SystemModelDecoder(json.JSONDecoder):
    """Decoder used in tessif system model deserialization."""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.tuple_hook, *args, **kwargs)

    def parse_tuple(self, tpl):
        """Parse Tessif's various tuple stirngs."""
        if "inf" in tpl:
            tpl = tpl.replace("inf", "'inf'")

        tpl = literal_eval(tpl)

        if "inf" in tpl:
            lst = [float("inf") if item == "inf" else item for item in tpl]
            tpl = tuple(lst)

        return tpl

    def parse_edge_key(self, edge_string):
        """Parse the edge string key."""
        # remove stringified container strings
        remove_chars = "[]()'"

        # create a translation table that maps each character to None
        translation_table = str.maketrans("", "", remove_chars)

        # remove the container string characters using the translation table
        destringified_edge = edge_string.translate(translation_table)

        # split the edge string in source and target and create the edge
        edge = Edge(*(item.strip() for item in destringified_edge.split(",")))

        return edge

    def tuple_hook(self, d):
        """Modify tuple decoding."""
        for key, value in d.copy().items():
            if isinstance(value, str):
                # check if value represents a tuple or list
                if value.startswith("(") and value.endswith(")"):
                    # parse tuple string
                    value = self.parse_tuple(value)

            if isinstance(key, str):
                if key.startswith("(") and key.endswith(")"):
                    # parse tuple string
                    d.pop(key)
                    key = self.parse_edge_key(key)

            d[key] = value
        return d
