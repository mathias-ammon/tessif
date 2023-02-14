# tessif/frused/paths.py
"""Tessif's most used paths.

:mod:`~tessif.frused.paths` is a :mod:`tessif` subpackage aggregating
frequently used path implementations for conveniently accessing utilities and
data coming with tessif.
"""
import inspect
import os
import pathlib
import sys

import ittools


def find_subpath_incwd(
    path,
    includes=("tessif",),
    excludes=(".git",),
):
    """Find location of  given path.

    Credit to: https://stackoverflow.com/a/41546830

    Note
    -----
    To make this utility work os independently it is advised to supply
    path using :func:`os.path.join`.

    Parameters
    ----------
    path : str
        String representation of the directory/file to find the path for.
        Supplying this paremter us ing :func:`os.path.join` makes this
        utility platform independent
    includes : :class:`~collections.abc.Iterable`, str
        String or iterable of strings that should be part of the
        found path.
    exludes : :class:`~collections.abc.Iterable`, str
        String or iterable of strings that should **not** be part of the
        found path.

    Return
    ------
    found_paths : list
        List of found paths
    """
    excludes = ittools.itrify(excludes)
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)

    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(os.getcwd())

    candidates = list(
        pathlib.Path(pathlib.Path(datadir).parent).glob(os.path.join("**", path))
    )

    found_paths = [
        candidate.as_posix()
        for candidate in candidates
        if not any(exclude in candidate.as_posix() for exclude in excludes)
        and all(include in candidate.as_posix() for include in includes)
    ]
    return found_paths


root_dir = os.path.normpath(
    os.path.join(
        inspect.getfile(inspect.currentframe()).split("paths")[0],
        "..",
    )
)
""" Tessif's root directory."""

tessif_dir = os.path.join(os.path.expanduser("~"), ".tessif.d")
logging_file = os.path.join(tessif_dir, "logs", "tessif_log.log")
