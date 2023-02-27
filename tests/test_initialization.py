# tests/test_initialization.py
"""Test proper tessif initialization."""
import os
import subprocess

import pytest


def test_dry_init():
    """Test for a succesful dry init run."""
    return_value = subprocess.run(
        ["tessif", "init", "--dry"],
        capture_output=True,
        text="True",  # open stderr as text
    )

    succes_log = "Succesfully initialized tessif's working directory"

    assert ".tessif.d" in return_value.stderr
    assert succes_log in return_value.stderr
    assert return_value.returncode == os.EX_OK


def test_dry_supplied_folder_init():
    """Test for succesfull dry run when supplying a custom folder."""
    return_value = subprocess.run(
        ["tessif", "init", "--dry", "--tessif_directory", "~/pytest_tessif_dir"],
        capture_output=True,
        text="True",  # open stderr as text
    )

    succes_log = "Succesfully initialized tessif's working directory"

    assert "pytest_tessif_dir" in return_value.stderr
    assert succes_log in return_value.stderr
    assert return_value.returncode == os.EX_OK


def test_supplied_folder_init(tmpdir):
    """Test for succesfull init run when supplying a custom folder."""

    tessif_folder = os.path.join(tmpdir, "pytest_tessif_dir")
    return_value = subprocess.run(
        ["tessif", "init", "--tessif_directory", tessif_folder],
        capture_output=True,
        text="True",  # open stderr as text
    )

    succes_log = "Succesfully initialized tessif's working directory"

    assert tessif_folder in return_value.stderr
    assert succes_log in return_value.stderr
    assert return_value.returncode == os.EX_OK
    assert os.path.isdir(tessif_folder)
