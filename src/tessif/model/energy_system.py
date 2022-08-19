# src/tessif/model/energy_system.py
# pylint: disable=too-few-public-methods
"""Dummy energy_system module to enebale tessif-examples."""


class AbstractEnergySystem:
    """Dummy energy system.

    Parameters
    ----------
    kwargs:
        Key word arguments
    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", "dummy_es")
