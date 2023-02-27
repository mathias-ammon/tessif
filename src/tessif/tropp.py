# src/tessif/tropp.py
"""Tessif's TRansform Optimize and Post-Process warppers."""

import importlib
import json

import tessif.frused.configurations


def transform(tessif_system_model, plugin, trans_ops=None, node_uid_style="name"):
    """
    Transform a tessif system model into one of the registered ESSMOS plugins.

    Parameters
    ----------
    tessif_system_model : :class:`tessif.system_model`
        Tessif system model to be transformed.
    plugin : str
        String specifying on of the supported ESSMOS plugins.
    trans_ops : dict
        Dictionairy holding transformation options. Passed to plugin transform
        utility as keyword arguments.
    node_uid_style: str, default="name"
        Node uid style used for identifying the individual components.
        See also :attr:`tessif.frused.namedtuples.node_uid_styles`
    """
    # perform runtime import
    module_name = plugin.replace("-", "_")
    plugin_module = importlib.import_module(module_name)

    # respect udi style
    tessif.frused.configurations.node_uid_style = node_uid_style

    # parse trans_ops
    if not trans_ops:
        trans_ops = {}

    # is this is called via the cli interface, transops neeed to be
    # reinitiated as dict
    if isinstance(trans_ops, str):
        trans_ops = json.loads(trans_ops)

    tool_system_model = plugin_module.transform(tessif_system_model, **trans_ops)

    return tool_system_model


def optimize(plugin_system_model, plugin, opt_ops=None):
    """Optimize the ESSMOS system model.

    Parameters
    ----------
    opt_ops : dict
        Dictionairy holding solver options.
    """
    module_name = plugin.replace("-", "_")
    plugin_module = importlib.import_module(module_name)

    optimized_system_model = plugin_module.optimize(plugin_system_model)

    return optimized_system_model


def post_process(optimized_plugin_system_model, plugin):
    """Help."""
    module_name = plugin.replace("-", "_")
    # plugin_module = importlib.import_module(module_name)

    post_process = importlib.import_module(f"{module_name}.post_process")

    global_resultier = post_process.IntegratedGlobalResultier(
        optimized_plugin_system_model
    )

    all_resultier = post_process.AllResultier(optimized_plugin_system_model)

    return global_resultier, all_resultier
