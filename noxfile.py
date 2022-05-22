# noxfile.py
"""Configure nox sessions."""

# standard library
import tempfile

# third pary packages
import nox

# local packages

# define default sessions:
nox.options.sessions = "lint", "tests", "noxfile.py", "docs/conf.py"


def install_with_constraints(session, *args, **kwargs):
    """Install packages constrained by Poetry's lock file."""
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
    """Run test suite."""
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
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "darglint",
    )
    # installs flak8 when 'nox -rs lint' is called
    session.run("flake8", *args)


@nox.session(python="3.10")
def black(session):
    """Reformat code using black."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.10")
def xdoctest(session):
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest", "pygments")
    session.run("python", "-m", "xdoctest", "tessif", *args)


@nox.session(python="3.10")
def docs(session):
    """Build the documentation."""
    install_with_constraints(session, "sphinx")
    session.run("sphinx-build", "docs", "docs/_build")
