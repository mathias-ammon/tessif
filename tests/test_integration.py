# tests/test_integration.py
"""Test proper tessif plugin integration."""
import os
import subprocess

import pytest

plugins = [
    "tessif-oemof-4-4",
    "tessif-pypsa-0-19-3",
    "tessif-fine-2-2-2",
    "tessif-calliope-0-6-6post1",
]


@pytest.mark.parametrize("plugin", plugins)
def test_dry_integration(plugin):
    """Test succesfull cli.integrate(dry=True) run."""
    return_value = subprocess.run(
        ["tessif", "integrate", "--dry", plugin],
        capture_output=True,
        text="True",  # open stderr as text
    )

    succes_log = "Succesfully added plugin"

    assert plugin in return_value.stderr
    assert succes_log in return_value.stderr
    assert return_value.returncode == os.EX_OK


@pytest.mark.parametrize("plugin", plugins)
def test_supplied_folder_integration(plugin, tmpdir):
    """Test succesfull cli.integrate(venv_dir=custom_dir) run."""
    cstm_dir = os.path.join(tmpdir, "pytest_tessif_dir", "plugin-venvs")
    return_value = subprocess.run(
        ["tessif", "integrate", "--venv_dir", cstm_dir, plugin],
        capture_output=True,
        text="True",  # open stderr as text
    )

    succes_log = f"Succesfully added plugin {plugin} to {cstm_dir}"

    assert plugin in return_value.stderr
    assert succes_log in return_value.stderr
    assert return_value.returncode == os.EX_OK
    assert os.path.isdir(cstm_dir)
