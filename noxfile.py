# noxfile.py

# standard library
import tempfile

# third pary packages
import nox

# local packages

# define default sessions:
nox.options.sessions = "lint", "tests"


def install_with_constraints(session, *args, **kwargs):
    """Wrapper for using poetry pins to nox session dependency installs."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",  # requ for working with pip resolver
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.10")
def tests(session):
    """Nox test session.

    Install package dependencies using poetry and testing dependies using the
    install_with_constraints wrapper.
    """
    args = session.posargs or [
        "--cov",
        "-m",
        "not e2e and not con and not slow",
        # add markers as "and not ..."
    ]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    )
    session.run("pytest", *args)


# locations to run linting and formatting on:
locations = "src", "tests", "noxfile.py"


@nox.session(python="3.10")
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-isort",
    )
    # installs flak8 when 'nox -rs lint' is called
    session.run("flake8", *args)


@nox.session(python="3.10")
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)
