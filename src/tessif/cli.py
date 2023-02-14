# src/tessif/cli.py
"""Module providing the Tessif Command Line Interface (CLI)."""
import importlib
import os
import pickle
import subprocess
import venv

import click

import tessif.logging as tessif_logging  # nopep8
from tessif.frused.paths import tessif_dir

logger = tessif_logging.logger


@click.group()
def main_cli_entry():
    """Tessif-Command main entry point."""
    pass


@main_cli_entry.command()
@click.option(
    "-d",
    "--tessif_directory",
    help="(Optional) Venv directory the plugin will be installed into.",
    default="~/.emacs.d/",
    show_default=True,
)
def init(tessif_directory=None):
    """Initialize Tessif's working directory."""
    if not tessif_directory:
        tessif_directory = os.path.join(os.path.expanduser("~"), ".tessif.d")
    click.echo(f"Initializing Tessif's main directory at {tessif_directory}")


@main_cli_entry.command()
@click.argument("plugin")
@click.option(
    "-vd",
    "--venv_dir",
    help="(Optional) Venv directory the plugin will be installed into.",
    default=None,
    show_default=True,
)
def install(plugin, venv_dir=None):
    """Install ESSMOS-Plugin."""
    if not venv_dir:
        venv_dir = os.path.join(tessif_dir, "plugin-venvs", plugin)
    python_bin = os.path.join(venv_dir, "bin", "python")
    venv.create(venv_dir, upgrade_deps=True, with_pip=True)
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


@main_cli_entry.command()
@click.option(
    "--directory",
    help="Directory the system_model.tsf and the results are/will be stored in",
    default=tessif_dir,
    show_default=True,
)
@click.option(
    "-q",
    "--quiet",
    help="Silences the stdout info level logging",
    is_flag=True,
)
@click.argument("plugin")
def tropp(directory, plugin, quiet):
    """Transform Optimize and Post-Process."""
    if quiet:
        tessif_logging.set_logger_level(logger, tessif_logging.logging.WARNING)

    system_model_location = os.path.join(directory, "tessif_system_model.tsf")
    all_resultier_location = os.path.join(directory, "all_resutlier.alr")
    igr_resultier_location = os.path.join(directory, "igr_resultier.igr")
    opt_sysmod_location = os.path.join(directory, "optimized_system_model.osm")

    logger.info("TRansform Optimize and Post-Process!\n")

    module_name = plugin.replace("-", "_")
    plugin_module = importlib.import_module(module_name)

    import oemof.solph

    logger.info("Using Plugin:")
    logger.info(f"{plugin} version {plugin_module.__version__}\n")
    logger.info("Using the modelling suit:")
    logger.info(f"oemof.solph version {oemof.solph.__version__}\n")

    logger.info("On System Model Stored In:")
    logger.info(system_model_location)
    logger.info("")

    from tessif.system_model import AbstractEnergySystem

    restored_es = AbstractEnergySystem(uid="This Instance Is Restored")
    restored_es.unpickle(system_model_location)
    logger.info("Succesfully deserialized tessif system model!")
    logger.info("Nodes present in the tessif system model:")
    logger.info([node.uid.name for node in restored_es.nodes])
    logger.info("")

    # t2o = importlib.import_module(f"{module_name}.tsf2omf")
    tool_system_model = plugin_module.transform(restored_es)

    logger.info("Nodes present in the oemof system model:")
    logger.info([str(node) for node in tool_system_model.nodes])

    optimized_system_model = plugin_module.optimize(tool_system_model)

    logger.info("Optimization Succesfull!")
    pickle.dump(optimized_system_model, open(opt_sysmod_location, "wb"))
    logger.info(f"Stored optmized system model to {opt_sysmod_location}")

    logger.info("Post-Process Tool System Model")
    post_process = importlib.import_module(f"{module_name}.post_process")
    global_resultier = post_process.IntegratedGlobalResultier(optimized_system_model)
    global_resultier.pickle(igr_resultier_location)
    logger.info(f"Stored global results to {igr_resultier_location}")

    all_resultier = post_process.AllResultier(optimized_system_model)
    all_resultier.pickle(all_resultier_location)
    logger.info(f"Stored all other results to {all_resultier_location}")
