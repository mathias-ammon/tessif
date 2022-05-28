# noxfile.py
"""Configure nox sessions."""

# standard library
import shutil
import tempfile
from pathlib import Path
from textwrap import dedent

# third pary packages
import nox

# local packages

# define default sessions:
nox.options.sessions = (
    "pre-commit",
    "lint",
    "tests",
    "xdoctest",
    "docs_rebuild",
)


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
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python="3.10")
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
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
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.10")
def docs_live(session):
    """Build and serve the documentation with live reloading on changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)


@nox.session(python="3.10")
def docs_rebuild(session):
    """Rebuild the entire sphinx documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )
    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.10")
def coverage(session):
    """Produce coverage report."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")


@nox.session(python="3.10")
def codecov(session):
    """Produce coverage report and try uploading to codecov."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


def activate_virtualenv_in_precommit_hooks(session):
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Parameters
    ----------
    session
        The Session object.
    """
    assert session.bin is not None  # noqa: S101

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@nox.session(name="pre-commit", python="3.10")
def precommit(session):
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    install_with_constraints(
        session,
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
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)
