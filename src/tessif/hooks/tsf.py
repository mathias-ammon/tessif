# tessif/frused/hooks/tsf.py
"""Tessif's tessif-system-model hooks.

:mod:`~tessif.frused.hooks.tsf` is a :mod:`tessif` module aggregating
mod:`tessif energy system specific <tessif.model.energy_system>` hooks to
change tessif energy systems after their creation.

Usually used for auto comparing a singular tessif energy system on
contradicting model assumptions. Like for example in :ref:`AutoCompare_HH`.
"""
import tessif.model.components as comps
from tessif.model.energy_system import AbstractEnergySystem


def reparameterize_components(es, components=None):
    """Reparameterize tessif-system-model components after its creation.

    Parameters
    ----------
    es: :class:`tessif.model.energy_system.AbstractEnergySystem`
        The tessif energy system that is to be reparameterized.
    components: dict, None, default=None
        Dictionairy of dictionairies keyeing parameter and value
        combination by :attr:`component uid <tessif.frused.namedtuples.Uid>`
        string representation. If none, an empty dictionairy is used.

    Examples
    --------
    Use :ref:`tessifs example hub <Examples>` to create a minimum working
    example:

    >>> from tessif_examples.basic import create_mwe()
    >>> mwe = create_mwe()

    Check the components that are to be reparamterized:

    >>> for transformer in mwe.transformers:
    ...     print(transformer.uid)
    ...     print(transformer.flow_costs)
    ...     print(transformer.conversions)
    Generator
    {'electricity': 2, 'fuel': 0}
    {('fuel', 'electricity'): 0.42}

    >>> for sink in mwe.sinks:
    ...     print(sink.uid)
    ...     print(sink.flow_rates)
    Demand
    {'electricity': MinMax(min=10, max=10)}

    Reparameterize the mwe:

    >>> reparameterized_mwe = reparameterize_components(
    ...     es=mwe,
    ...     components={
    ...         'Generator': {
    ...             'flow_costs': {'electricity': 3, 'fuel': 0},
    ...             'conversions': {('fuel', 'electricity'): 0.43},
    ...         },
    ...         'Demand': {
    ...             'flow_rates': {'electricity': (11, 11)},
    ...         }
    ...     },
    ... )

    Check the reparemterized components:

    >>> for transformer in reparameterized_mwe.transformers:
    ...     print(transformer.uid)
    ...     print(transformer.flow_costs)
    ...     print(transformer.conversions)
    Generator
    {'electricity': 3, 'fuel': 0}
    {('fuel', 'electricity'): 0.43}

    >>> for sink in reparameterized_mwe.sinks:
    ...     print(sink.uid)
    ...     print(sink.flow_rates)
    Demand
    {'electricity': MinMax(min=11, max=11)}
    """
    if not components:
        components = dict()
    # turn generator into list for recreating the es later
    nodes = list(es.nodes)
    # iterate through the requested components...
    for uid in components.keys():

        # ... and through all nodes inside the es...
        for idx, node in enumerate(nodes.copy()):

            # ... to see if the requested component is inside the es
            if uid == str(node.uid):

                # yes it is, so ...
                # create a uid mapping for recreating the component
                comp_uid = node.uid._asdict()

                # and copy all the attributes so they can be manipulated w/o
                # interferring with the original es
                attributes = node.attributes.copy()

                # remove the uid part since it is handled above
                attributes.pop("uid")

                # iterate over requested parameters
                for parameter, value in components[uid].items():

                    # print('changing parameter', parameter, # future log
                    #       'of comp:', uid) # future log
                    # print('from:', attributes[parameter]) # future log

                    # and chang thir value acoordingly
                    attributes[parameter] = value

                    # print('to:', attributes[parameter]) # future log

                # infer reparameterized components type in a way ...
                ntype = str(type(node)).split(".")[-1].replace("'>", "")

                # its constructor can be allocated dynamically
                # and the reparameterized component created
                new_comp = getattr(comps, ntype)(
                    **comp_uid,
                    **attributes,
                )

                # remove the old component from the list
                nodes.pop(idx)

                # and replace it by the new one
                nodes.append(new_comp)

    # recreate the enerergy system ...
    reparameterized_es = AbstractEnergySystem.from_components(
        uid=f"reparameterized_{es.uid}",
        components=nodes,
        timeframe=es.timeframe,
        global_constraints=es.global_constraints,
    )

    # ... and return the now reparameterized energy system.
    return reparameterized_es
