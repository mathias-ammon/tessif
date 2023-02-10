# tessif/frused/hooks/ppsa.py
# -*- coding: utf-8 -*-
"""
:mod:`~tessif.frused.hooks.ppsa` is a :mod:`tessif` module aggregating
:ref:`pypsa specific <Models_Pypsa>` hooks to improve it's integration
into tessif.
"""
import pypsa
import numpy as np


def enforce_uid():
    """
    test
    """
    pass


def add_flow_bound_emissions(attribute_dict):
    """
    Pre simulation hook for extending pypsa components to enable flow specific
    emissions.

    After applying this hook, all pypsa energy system components will have
    an additional input parameter called ``flow_emissions`` which allows
    allocating flow specific emission values.

    The emission values are post processed using the
    :class:`~tessif.transform.es2mapping.ppsa.FlowResultier`.

    The overriding code was inspired by the `pypsa chp example
    <https://www.pypsa.org/examples/chp-fixed-heat-power-ratio.html>`_

    Parameters
    ----------
    attribute_dict: dict
        Dictionary returned by pypsa.components.component_attrs.
        Used for chaining hooks.

    Return
    ------
    custom_attributes: dict
        Extended :paramref:`~add_flow_bound_emissions.attribute_dict` carrying
        the parameters for using flow bound emission values.

    """
    co2_bound_components = ['Generator', 'Link', 'StorageUnit']

    # bus flow emissions
    for component in co2_bound_components:
        attribute_dict[component].loc["flow_emissions"] = [
            "static",                   # type
            "t_CO2eq/MW",               # unit
            0.,                         # default
            "flow specific emissions",  # docstring
            "Input (optional)"          # input output and required/optional
        ]

    return attribute_dict


def add_siso_transfromer_type(attribute_dict):
    """
    Pre simulation hook for extending pypsa links to act like siso
    transfromers.

    After applying this hook, all pypsa energy system components will have
    an additonal input parameter called ``siso_transformer`` as well as
    ``flow_costs`` which allows single input single output post processing.

    The overriding code was inspired by the `pypsa chp example
    <https://www.pypsa.org/examples/chp-fixed-heat-power-ratio.html>`_

    Parameters
    ----------
    attribute_dict: dict
        Dictionairy returned by pypsa.components.component_attrs.
        Used for chaining hooks.

    Return
    ------
    custom_attributes: dict
        Extended :paramref:`~add_siso_transfromer_label.attribute_dict`
       carrying the parameters for using the extendend transfromer type.

    """
    siso_transformer_components = ['Link', ]

    # bus flow emissions
    for component in siso_transformer_components:
        # adding the option to tell the post processors about multiple inputs
        attribute_dict[component].loc["siso_transformer"] = [
            "bool",                           # type
            np.nan,                           # unit
            False,                            # default
            "Link has 1 input and 1 output",  # docstring
            # input output and required/optional
            "Input (optional)"
        ]

        attribute_dict[component].loc["flow_costs"] = [
            "static",               # type
            "€/MW",                 # unit
            0.,                     # default
            "flow specific costs",  # docstring
            "Input (optional)"      # input output and required/optional
        ]

        attribute_dict["Link"].loc[f"expansion_costs"] = [
            "static",  # type
            "€/MW",  # unit
            0.,  # default
            "expansion cost",  # docstring
            "Input (optional)"  # input output and required/optional
        ]

    return attribute_dict


def extend_number_of_link_interfaces(attribute_dict, additional_interfaces=1):
    """
    Pre simulation hook for extending pypsa links to enable using them as
    simple chps.

    After applying this hook, all pypsa energy system links will have
    1 input and up to 2 outputs (with the first beeing mandatory and second
    beeing optional).

    It will also add a link attribute called ``siso_transformer`` indicating
    whether a link is a `singular input, singnular output (siso)` transformer
    or a :class:`Connector style object <tessif.model.components.Connector>`
    where singular input and singular output are both bidirecctional.

    The overriding code was taken from the `pypsa chp example
    <https://www.pypsa.org/examples/chp-fixed-heat-power-ratio.html>`_
    .

    Parameters
    ----------
    attribute_dict: dict
        Dictionairy returned by pypsa.components.component_attrs.
        Used for chaining hooks.

    additional_interfaces: int, default=1
        Integer specifying the number of additional interfaces added to the
        link component.

    Return
    ------
    custom_attributes: dict
        Extended :paramref:`~extend_number_of_link_interfaces.attribute_dict`
        carrying the parameters for using flow bound emisison values.

    """
    # bus 0 to 1 flow costs
    attribute_dict["Link"].loc["flow_costs"] = [
        "static",               # type
        "€/MW",                 # unit
        0.,                     # default
        "flow specific costs",  # docstring
        "Input (optional)"      # input output and required/optional
    ]

    # bus 0 to 1 expansion cost
    attribute_dict["Link"].loc[f"expansion_costs"] = [
        "static",              # type
        "€/MW",                # unit
        0.,                    # default
        "expansion cost",      # docstring
        "Input (optional)"     # input output and required/optional
    ]

    # adding the option to tell the post processors about multiple outputs
    attribute_dict["Link"].loc["multiple_outputs"] = [
        "bool",                        # type
        np.nan,                        # unit
        False,                         # default
        "Link uses multiple outputs",  # docstring
        "Input (optional)"             # input output and required/optional
    ]

    # # adding the option to tell the post processors about multiple inputs
    # attribute_dict["Link"].loc["multiple_inputs"] = [
    #     "bool",                        # type
    #     np.nan,                        # unit
    #     False,                         # default
    #     "Link uses multiple inputs",  # docstring
    #     "Input (optional)"             # input output and required/optional
    # ]

    # adding the option to tell the post processors about multiple inputs
    attribute_dict["Link"].loc["siso_transformer"] = [
        "bool",                           # type
        np.nan,                           # unit
        False,                            # default
        "Link has 1 input and 1 output",  # docstring
        "Input (optional)"                # input output and required/optional
    ]

    # add a new link interface for each one requested:
    for i in range(additional_interfaces):

        # connecting bus attribute
        attribute_dict["Link"].loc[f"bus{2+i}"] = [
            "string",           # type
            np.nan,             # unit
            np.nan,             # default
            "2nd bus",          # docstring
            "Input (optional)"  # input/output and required/optional
        ]

        # bus 0 to 2+i efficiency
        attribute_dict["Link"].loc[f"efficiency{2+i}"] = [
            "static or series",     # type
            "per unit",             # unit
            1.,                     # default
            "2nd bus efficiency",   # docstring
            "Input (optional)"      # input/output and required/optional
        ]

        # bus 0 to 2+i flow costs
        attribute_dict["Link"].loc[f"flow_costs{2+i}"] = [
            "static",            # type
            "€/MW",              # unit
            0.,                  # default
            "addit. flow cost",  # docstring
            "Input (optional)"   # input output and required/optional
        ]

        # bus 0 to 2+i flow emissions
        attribute_dict["Link"].loc[f"flow_emissions{2+i}"] = [
            "static",            # type
            "t_CO2/MW",          # unit
            0.,                  # default
            "addit. flow cost",  # docstring
            "Input (optional)"   # input output and required/optional
        ]

        # bus 0 to 2+i installed capacities
        attribute_dict["Link"].loc[f"p_nom{2+i}"] = [
            "static",            # type
            "MW",                # unit
            0.,                  # default
            "addit. capacity",   # docstring
            "Input (optional)"   # input output and required/optional
        ]

        # bus 0 to 2+i expansion cost
        attribute_dict["Link"].loc[f"expansion_costs{2+i}"] = [
            "static",              # type
            "€/MW",                # unit
            0.,                    # default
            "2nd expansion cost",  # docstring
            "Input (optional)"     # input output and required/optional
        ]

        # bus 0 to 2+i result
        attribute_dict["Link"].loc[f"p{2+i}"] = [
            "series",          # type
            "MW",              # unit
            0.,                # default
            "2nd bus output",  # docstring
            "Output"           # input output and required/optional
        ]

    return attribute_dict


def constrain_extended_link_interfaces(additional_interfaces):
    """
    Pre simulation hook to constrain the additonal interfaces added by
    :func:`extend_number_of_link_interfaces`.

    Callable designed to be passed to :attr:`pypsa.Network.lopf` as
    ``extra_functionality``.

    The code was inspired by the pypsa `Power to Gas with Heat Coupling
    <https://pypsa.readthedocs.io/en/latest/examples/power-to-gas-boiler-chp.html>`_
    example
    """

    # # constrain link interface for each one requested:
    # for i in range(additional_interfaces):

    #     # Guarantees c_m p_b1  \leq p_g1
    #     rule = network.links.at["boiler", "efficiency"]

    #     def backpressure(model, snapshot):
    #         return c_m*network.links.at["boiler", "efficiency"]*model.link_p["boiler", snapshot] <= network.links.at["generator", "efficiency"]*model.link_p["generator", snapshot]

    #     network.model.backpressure = Constraint(
    #         list(snapshots), rule=backpressure)
