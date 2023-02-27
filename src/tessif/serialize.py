"""Store / Serialize tessif features."""
import json

import numpy as np
import pandas as pd

from tessif.frused.namedtuples import Edge


class ResultierEncoder(json.JSONEncoder):
    """Handle resultier encoding (serialization)."""

    def edge_to_string(self, obj):
        """Transform edge to list in quotes."""
        if isinstance(obj, Edge):
            return f"[{obj.source}, {obj.target}]"
        else:
            return obj

    def default(self, obj):
        """Modify value parsing."""
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_json(orient="split")

        return super().default(obj)

    def _encode(self, obj):
        """Modify key parsing."""
        if isinstance(obj, dict):

            def parse_edge(obj):
                return self._encode(
                    self.edge_to_string(obj) if isinstance(obj, Edge) else obj
                )

            dct = {parse_edge(k): parse_edge(v) for k, v in obj.items()}

            return dct
        else:
            return obj

    def encode(self, obj):
        """Modify key parsing by calling _encode."""
        return super().encode(self._encode(obj))


class SystemModelEncoder(json.JSONEncoder):
    """Handle resultier encoding (serialization)."""

    def default(self, obj):
        """Modify value parsing."""
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_json(orient="split")

        if isinstance(obj, frozenset):
            return tuple(obj)

        if isinstance(obj, np.array):
            return tuple(obj)

        return super().default(obj)

    def tuple_to_string(self, obj):
        """Transform tuple to tuple-string in quotes."""
        if isinstance(obj, tuple):
            lst = [
                tuple(entry) if isinstance(entry, np.ndarray) else entry
                for entry in obj
            ]
            return str(tuple(lst))

        if isinstance(obj, type(np.array)):
            return str(tuple(obj))

        else:
            return obj

    def _encode(self, obj):
        """Modify key parsing."""
        if isinstance(obj, dict):

            def parse_tuples(obj):
                return self._encode(
                    self.tuple_to_string(obj)
                    if isinstance(obj, (tuple, type(np.array)))
                    else obj
                )

            dct = {parse_tuples(k): parse_tuples(v) for k, v in obj.items()}

            return dct
        else:
            return obj

    def encode(self, obj):
        """Modify key parsing by calling _encode."""
        return super().encode(self._encode(obj))
