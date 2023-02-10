import nox
import nox_poetry


@nox_poetry.session(
    python=["3.8", "3.9", "3.10"],
    reuse_venv=True,
    name="tessif-oemof-4.4-python",
)
def tsf_omf_44(session):
    plugin = "tessif-oemof-4-4"
    sysmod_location = session.posargs

    # install tessif using poetry
    session.run(
        "poetry",
        "install",
        "--only",
        "oemof-0-4-4",
        external=True,
    )

    # install tessif-oemof-4.4 using pip
    session.install(plugin)
    session.install("matplotlib")

    # print(session.name)
    # print(sysmod_location)

    # run the tessif optimize cli command to tropp the system model
    session.run(
        "tessif",
        "tropp",
        "--system_model_location",
        sysmod_location[0],
        plugin,
    )
