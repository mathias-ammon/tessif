"""Test succesful tropping using Tessif."""
import pytest
from tessif_examples import basic, scientific

import tessif.hooks.tsf as tessif_hooks

PLUGINS = [
    "tessif-oemof-4-4",
    "tessif-pypsa-0-19-3",
    "tessif-fine-2-2-2",
    "tessif-calliope-0-6-6post1",
]

basic_creates = [attr for attr in dir(basic) if "create" in attr]


@pytest.mark.parametrize("system_model_name", basic_creates)
def test_basic_es_tropping(system_model_name):
    """Test tropping using the basic tessif-example sysmods."""
    tsf_sys_mod = getattr(basic, system_model_name)()

    trans_ops = None
    if tsf_sys_mod.uid == "Fully_Parameterized_Working_Example":
        tsf_sys_mod = tessif_hooks.reparameterize_components(
            es=tsf_sys_mod,
            components={"Battery": {"initial_soc": 9}},
        )

    if tsf_sys_mod.uid == "Transformer-Timeseries-Example":
        trans_ops = {"forced_links": ("Transformer",)}

    if tsf_sys_mod.uid == "Two Transformer Grid Example":
        trans_ops = {
            "forced_links": ("H2M", "M2H"),
            "excess_sinks": ("HV-XS", "MV-XS"),
        }

    results = tsf_sys_mod.tropp(
        plugins=PLUGINS,
        quiet=True,
        trans_ops=trans_ops,
    )

    assert isinstance(results, dict)


scientific_creates = [attr for attr in dir(scientific) if "create" in attr]


@pytest.mark.parametrize("system_model_name", scientific_creates)
def test_scientific_es_tropping(system_model_name):
    """Test tropping using the scientific tessif-example sysmods."""
    tsf_sys_mod = getattr(basic, system_model_name)()

    results = tsf_sys_mod.tropp(
        plugins=PLUGINS,
        quiet=True,
    )

    assert isinstance(results, dict)
