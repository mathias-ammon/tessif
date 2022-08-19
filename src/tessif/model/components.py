# src/tessif/model/components.py
# pylint: disable=too-few-public-methods
"""Dummy components module to enebale tessif-examples."""


class Bus:
    """Dummy Bus component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_bus")
        self.ctype = "bus"


class Source:
    """Dummy Source component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_source")
        self.ctype = "source"


class Sink:
    """Dummy Sink component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_sink")
        self.ctype = "sink"


class Transformer:
    """Dummy Transformer component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_transformer")
        self.ctype = "transformer"


class Storage:
    """Dummy Storage component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_storage")
        self.ctype = "storage"


class Connector:
    """Dummy Connector component."""

    def __init__(self, **kwargs):
        self.uid = kwargs.get("name", "dummy_connector")
        self.ctype = "connector"
