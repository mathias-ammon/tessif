# src/tessif/cli.py
"""Module providing the Tessif Command Line Interface (CLI)."""
import importlib

import click


@click.group()
def main_cli_entry():
    """Tessif-Command main entry point."""
    pass


@main_cli_entry.command()
def greet():
    """Greet the world."""
    click.echo("Hello World!")


@main_cli_entry.command()
@click.option(
    "--system_model_location",
    help="Tessif System-Model Location",
)
@click.argument("plugin")
def tropp(system_model_location, plugin):
    """TRansform Optimize and Post-Process."""
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


# if __name__ == '__main__':
#     main_cli_entry()
