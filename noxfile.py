# noxfile.py
"""Configure nox sessions."""

# standard library
import shutil
import tempfile
from pathlib import Path

# third pary packages
import nox
import nox_poetry

# local packages

# define default sessions:
nox.options.sessions = (
    "pre-commit",
    "lint",
    "pylint",
    "tests",
    "xdoctest",
    "safety",
    "docs_rebuild",
)


# deprecated with migration to nox-poetry:
# def install_with_constraints(session, *args, **kwargs):
#     """Install packages constrained by Poetry's lock file."""
#     with tempfile.NamedTemporaryFile() as requirements:
#         session.run(
#             "poetry",
#             "export",
#             "--dev",
#             "--format=requirements.txt",
#             "--without-hashes",  # requ for working with pip resolver
#             f"--output={requirements.name}",
#             external=True,
#         )
#         session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox_poetry.session(python="3.10")
def tests(session):
    """Run test suite."""
    args = session.posargs or [
        "--cov",
        "-m",
        "not e2e and not con and not slow",
        # append exlcuded markers as "and not ..."
    ]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "tessif-examples",
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    )
    session.run("pytest", *args)


# locations to run linting and formatting on:
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox_poetry.session(python="3.10")
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "darglint",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pyupgrade",
    )
    session.run("flake8", *args)


@nox_poetry.session(python="3.10")
def pylint(session):
    """Lint using pylint."""
    args = session.posargs or locations
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "pytest",
        "requests",
        "nox",
        "nox-poetry",
        "pylint",
    )
    session.run("pylint", "--output-format=colorized", "--recursive=y", *args)


@nox_poetry.session(python="3.10")
def black(session):
    """Reformat code using black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox_poetry.session(python="3.10")
def xdoctest(session):
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("xdoctest", "pygments")
    session.run("python", "-m", "xdoctest", "tessif", *args)


@nox_poetry.session(python="3.10")
def docs(session):
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "sphinx",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )
    session.run("sphinx-build", "docs", "docs/_build")


@nox_poetry.session(python="3.10")
def docs_live(session):
    """Build and serve the documentation with live reloading on changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
        "tessif-examples",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)


@nox_poetry.session(python="3.10")
def docs_rebuild(session):
    """Rebuild the entire sphinx documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "sphinx",
        "sphinx-click",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
        "tessif-examples",
    )
    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", "docs", "docs/_build")


@nox_poetry.session(python="3.10")
def coverage(session):
    """Produce coverage report."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")


@nox_poetry.session(python="3.10")
def codecov(session):
    """Produce coverage report and try uploading to codecov."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox_poetry.session(name="pre-commit", python="3.10")
def precommit(session):
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(
        "darglint",
        "black",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pyupgrade",
        "pytest",
        "requests",
        "nox",
        "nox-poetry",
        "pylint",
    )
    session.run("pre-commit", *args)


@nox_poetry.session(python="3.10")
def safety(session):
    """Scan dependencies for insecure packages using safety."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
