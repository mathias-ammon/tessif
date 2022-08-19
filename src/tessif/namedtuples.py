# src/tessif/namedtuples.py
# pylint: disable=invalid-name
"""Dummy named tuples file to enebale tessif-examples."""
import collections

MinMax = collections.namedtuple("MinMax", ["min", "max"])
"""
Corespondent minimum and maximum value pair. Usually used for energy system
value parings like flow limits (i.e: minimum and maximum flow boundaries).
"""

OnOff = collections.namedtuple("OnOff", ["on", "off"])
"""
Corespondent value pair for describing parameters dependent on a boolean
status. Usually used for energy system value parings describing nonconvex
behaviour like i.e: minimum uptime and downtime.
"""

InOut = collections.namedtuple("InOut", ["inflow", "outflow"])
"""
Corespondent inflow outflow value pair. Usually used for energy system value
parings describing different behaviours of the same component depending on in
or outflow like i.e: Storage efficiency
"""

PositiveNegative = collections.namedtuple(
    "PositiveNegative",
    ["positive", "negative"],
)
"""
Corespondent value pair for describing parameters dependent on directions
expressed as positive or negative. Usually used for energy system value
parings describing changes between timesteps like i.e: power production
gradients.
"""
