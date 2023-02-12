# src/tessif/cli.py
"""Module providing the Tessif Command Line Interface (CLI)."""
import importlib
import os
import venv
import subprocess
import click

PLUGIN = "tessif-oemof-4-4"

tessif_dir = os.path.join(os.path.expanduser("~"), ".tessif.d")
venv_dir = os.path.join(tessif_dir, "plugin-venvs", PLUGIN)
python_bin = os.path.join(venv_dir, "bin", "python")


@click.group()
def main_cli_entry():
    """Tessif-Command main entry point."""
    pass


@main_cli_entry.command()
def greet():
    """Greet the world."""
    click.echo("Hello World!")


@main_cli_entry.command()
@click.argument("plugin")
def install_plugin(plugin):
    venv.create(venv_dir, upgrade_deps=True, with_pip=True)
    subprocess.run(
        [
            python_bin,
            "-m",
            "pip",
            "install",
            plugin,
        ]
    )


@main_cli_entry.command()
@click.option(
    "--directory",
    help="Directory the system_model.tsf and the results are/will be stored in",
)
@click.argument("plugin")
def tropp(directory, plugin):
    """TRansform Optimize and Post-Process."""

    system_model_location = os.path.join(directory, "tessif_system_model.tsf")
    all_resultier_location = os.path.join(directory, "all_resutlier.alr")
    igr_resultier_location = os.path.join(directory, "igr_resultier.igr")

    click.echo("TRansform Optimize and Post-Process!\n")

    module_name = plugin.replace("-", "_")
    plugin_module = importlib.import_module(module_name)

    import oemof.solph

    click.echo("Using Plugin:")
    click.echo(f"{plugin} version {plugin_module.__version__}\n")
    click.echo("Using the modelling suit:")
    click.echo(f"oemof.solph version {oemof.solph.__version__}\n")

    click.echo("On System Model Stored In:")
    click.echo(system_model_location)
    click.echo()

    from tessif.model.energy_system import AbstractEnergySystem

    restored_es = AbstractEnergySystem(uid="This Instance Is Restored")
    msg = restored_es.unpickle(system_model_location)
    click.echo("Succesfully deserialized tessif system model!")
    click.echo("Nodes present in the tessif system model:")
    click.echo([node.uid.name for node in restored_es.nodes])
    click.echo()

    # t2o = importlib.import_module(f"{module_name}.tsf2omf")
    tool_system_model = plugin_module.transform(restored_es)

    click.echo("Nodes present in the oemof system model:")
    click.echo([str(node) for node in tool_system_model.nodes])

    optimized_system_model = plugin_module.optimize(tool_system_model)

    click.echo("Optimization Succesfull!")
    click.echo(f"Global Costs: {optimized_system_model.results['global']['costs']}")

    click.echo("Post-Process Tool System Model")
    post_process = importlib.import_module(f"{module_name}.post_process")
    global_resultier = post_process.IntegratedGlobalResultier(
        optimized_system_model)
    global_resultier.pickle(igr_resultier_location)
    click.echo(f"Stored global results to {igr_resultier_location}")

    all_resultier = post_process.AllResultier(optimized_system_model)
    all_resultier.pickle(all_resultier_location)
    click.echo(f"Stored all other results to {all_resultier_location}")


# if __name__ == '__main__':
#     main_cli_entry()
