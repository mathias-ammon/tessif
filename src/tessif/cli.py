# src/tessif/cli.py
"""Module providing the Tessif Command Line Interface (CLI)."""
import json
import logging
import os
import subprocess
import sys
import venv
from pathlib import Path

import click

import tessif.tropp
from tessif.frused.defaults import registered_plugins
from tessif.frused.paths import tessif_dir
from tessif.logging import create_logger, reset_basic_config
from tessif.serialize import ResultierEncoder
from tessif.system_model import AbstractEnergySystem

logger = create_logger(__name__)


@click.group()
def main_cli_entry():
    """Tessif-Command main entry point."""
    pass


@main_cli_entry.command()
@click.option(
    "-d",
    "--tessif-directory",
    help="(Optional) Venv directory the plugin will be installed into.",
    default="~/.tessif.d/",
    show_default=True,
)
@click.option(
    "--dry",
    help="Execute integration with actually installing anything",
    is_flag=True,
)
def init(tessif_directory=None, dry=False):
    """Initialize tessif's working directory."""
    if not tessif_directory:
        tessif_directory = tessif_dir

    # Create a Path object for the new folder
    working_directory = Path(tessif_directory)

    logger.info(
        "Attempting to initialize tessif's working directory at %s",
        working_directory,
    )

    if not dry:
        # Create the folder if it doesn't exist, with parents as needed
        working_directory.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Succesfully initialized tessif's working directory at %s",
        working_directory,
    )

    return sys.exit(os.EX_OK)


@main_cli_entry.command()
@click.argument("plugin")
@click.option(
    "-vd",
    "--venv_dir",
    help="(Optional) Venv directory the plugin will be installed into.",
    default=None,
    show_default=True,
)
@click.option(
    "--dry",
    help="Execute integration with actually installing anything",
    is_flag=True,
)
def integrate(plugin, venv_dir=None, dry=False):
    """Integrate ESSMOS-Plugin."""
    # Sanitize Plugin Input
    if plugin not in registered_plugins.keys():
        msg = " ".join(
            [
                f"Plugin {plugin} not recognized.",
                "Available plugins are:",
                *(plg for plg in registered_plugins.keys()),
            ]
        )
        raise KeyError(msg)
    else:
        plugin = registered_plugins[plugin]

    logger.info("Establish plugin venv directory at")
    if not venv_dir:
        venv_dir = os.path.join(tessif_dir, "plugin-venvs", plugin)

    logger.info("%s", venv_dir)

    python_bin = os.path.join(venv_dir, "bin", "python")
    logger.info("Initializing new python binary at %s", python_bin)

    if not dry:
        venv.create(venv_dir, upgrade_deps=True, with_pip=True)

    logger.info(
        "Succesfully created venv for plugin %s at %s",
        plugin,
        venv_dir,
    )

    logger.info(
        "Attempting to integrate plugin %s to %s using %s",
        plugin,
        venv_dir,
        python_bin,
    )

    if not dry:
        subprocess.run(
            [
                python_bin,
                "-m",
                "pip",
                "install",
                "-U",  # update plugin
                plugin,
            ]
        )
    else:
        logger.info("Performing a dry pip run:\n")
        subprocess.run(
            [
                python_bin,
                "-m",
                "pip",
                "install",
                "--dry-run",  # perfrom dry run
                plugin,
            ]
        )

    logger.info(
        "Succesfully added plugin %s to %s using %s",
        plugin,
        venv_dir,
        python_bin,
    )

    return sys.exit(os.EX_OK)


@main_cli_entry.command()
@click.argument("plugin")
@click.option(
    "-d",
    "--directory",
    help="Directory the system_model.tsf and the results are/will be stored in",
    default=os.path.join(tessif_dir, "tropp"),
    show_default=True,
)
@click.option(
    "-q",
    "--quiet",
    help="Silences the stdout info level logging",
    is_flag=True,
)
@click.option(
    "--trans_ops",
    help="Dictionairy holding the transformation options",
    default=None,
    show_default=True,
)
@click.option(
    "--opt_ops",
    help="Dictionairy holding the optimization options (not yet implemented)",
    default=None,
    show_default=True,
)
def tropp(plugin, directory, quiet, trans_ops, opt_ops):
    """Transform Optimize and Post-Process."""
    # Parse the arguments

    # logger.setLevel(logging.INFO)
    if quiet:
        logger.setLevel(logging.WARNING)

    # Create the folder if it doesn't exist, with parents as needed
    working_directory = Path(directory)
    working_directory.mkdir(parents=True, exist_ok=True)

    # initialize storage locations
    system_model_location = os.path.join(directory, "tessif_system_model.tsf")

    # start tropp process
    logger.info(60 * "-")
    logger.info("TRansform Optimize and Post-Process!")
    logger.info(f"Using Plugin: {plugin}")

    restored_sys_mod = AbstractEnergySystem.deserialize(
        json.load(open(system_model_location))
    )

    # restored_es = AbstractEnergySystem(uid="This Instance Is Restored")
    # restored_es.unpickle(system_model_location)

    # logger.info("On The System Model Stored In:")
    # logger.info(system_model_location)
    # logger.info("")

    logger.info(f"Transform to {plugin} System Model")
    plugin_system_model = tessif.tropp.transform(
        tessif_system_model=restored_sys_mod,
        plugin=plugin,
        trans_ops=trans_ops,
    )
    reset_basic_config()
    logger.info("Transformation Succesfull!\n")

    # lgers = logging.Logger.manager.loggerDict
    # for lger, value in lgers.items():
    #     print(lger, value)

    logger.info(f"Optimize {plugin} System Model")
    optimized_plugin_system_model = tessif.tropp.optimize(
        plugin_system_model=plugin_system_model,
        plugin=plugin,
        opt_ops=opt_ops,
    )
    logger.info("Optimization Succesful!\n")

    logger.info(f"Post-Process {plugin} System Model")
    global_resultier, all_resultier = tessif.tropp.post_process(
        optimized_plugin_system_model=optimized_plugin_system_model,
        plugin=plugin,
    )
    # post_opt_logger.disable = True
    # logger = create_logger(f"{__name__}.post_post_processing")
    logger.info("Post-Processing Succesful!\n")

    igr_resultier_location = os.path.join(directory, f"{plugin}_igr_resultier.igr")

    serialized_global_resultier = json.dumps(
        global_resultier.dct_repr(),
        cls=ResultierEncoder,
    )

    json.dump(
        serialized_global_resultier,
        fp=open(igr_resultier_location, "w"),
        # cls=ResultierEncoder,
    )
    logger.info(f"Stored global results to {igr_resultier_location}")

    all_resultier_location = os.path.join(directory, f"{plugin}_all_resutlier.alr")
    serialized_all_resultier = json.dumps(
        all_resultier.dct_repr(),
        cls=ResultierEncoder,
    )
    json.dump(
        serialized_all_resultier,
        fp=open(all_resultier_location, "w"),
        # cls=ResultierEncoder,
    )
    logger.info(f"Stored all other results to {all_resultier_location}")
    logger.info(60 * "-" + "\n")
