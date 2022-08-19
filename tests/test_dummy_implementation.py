# tests/test_end2end.py
"""Module for dumym implementation testing."""
import pytest

import tessif.namedtuples as nts
from tessif.model import components, energy_system


def test_energy_sysytem():
    """Test dummy energy system."""
    esys = energy_system.AbstractEnergySystem(uid="pytest_es")

    assert esys.uid == "pytest_es"


@pytest.mark.parametrize(
    "comp",
    [
        "Bus",
        "Sink",
        "Source",
        "Transformer",
        "Storage",
        "Connector",
    ],
)
def test_bus(comp):
    """Test dummy bus."""
    component = getattr(components, comp)(name=f"pytest_{comp}")

    assert component.uid == f"pytest_{comp}"


def test_minmax_namedtuple():
    """Test MinMax namedtuples."""
    ntpl = nts.MinMax(0, 1)
    assert ntpl.min == 0
    assert ntpl.max == 1


def test_onfoff_namedtuple():
    """Test MinMax namedtuples."""
    ntpl = nts.OnOff(0, 1)
    assert ntpl.on == 0
    assert ntpl.off == 1


def test_positivenegative_namedtuple():
    """Test MinMax namedtuples."""
    ntpl = nts.PositiveNegative(0, 1)
    assert ntpl.positive == 0
    assert ntpl.negative == 1


def test_inout_namedtuple():
    """Test MinMax namedtuples."""
    ntpl = nts.InOut(0, 1)
    assert ntpl.inflow == 0
    assert ntpl.outflow == 1
