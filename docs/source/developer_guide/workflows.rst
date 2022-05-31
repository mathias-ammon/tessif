.. _workflows:

Workflows (Nox and Poetry)
**************************

Following sections provide information on how to use the excellent
Hypermodern-Python_ project foundation proposed by `Claudio Jolowicz <cj>`_

.. contents:: Contents
   :backlinks: top
   :local:

Documentation
=============

This project uses Sphinx_ relying on docstrings_ in `NumPy Style`_ which get
inforced by flake8-docstrings_ and darglint_. Use Nox_ to conveniently build
the documentaiton inside the :file:`docs/_build` folder:

To tweak or add nox sessions, alter the :file:`noxfile.py` inside this
project's root directory.

nox -s docs -- Statically build whats new
-----------------------------------------

Build the documentation while only acutally rebuilding those files that
changed:

.. code:: console

   nox -s docs

nox -s docs_rebuild -- Statically build everything from scratch
---------------------------------------------------------------

Rebuild the entire documentation from scratch:

.. code:: console

   nox -s docs_rebuild

nox -s docs_live -- Dynamically build from scratch (once)
---------------------------------------------------------

Builts the documentation from scratch, servs it locally on port 8000, opens
your default browser on the main page (:file:`docs/_build/index.html`) and
rebuilts any pages live, that are subject to change (when saved to disk).

Invaluable when creating the documentation!

.. code:: console

   nox -s docs_live

Testing
=======

This project uses Nox_ to conveniently run both:

  - unittests_ via the defacto standard pytest_
  - doctests_  via xdoctest_

To tweak or add nox testing sessions, alter the :file:`noxfile.py` inside this
project's root directory.

nox -s tests -- Unittests
-------------------------
Unittests reside in :file:`tests/` inside the root directory of this project.
Make sure to provide docstrings (since they are enforced, heh!) and add new
test modules to :file:`docs/source/unittests.rst`.

Run all unittests using nox:

.. code:: console

   nox -s tests

nox -s xdoctests -- Doctests
----------------------------
Me personally, I love doctests. I thinks they are the most natural form of
testing. Since archiev both with them: enforced tests and pretty,
copy-pastable examples inside your documentation.

Run all doctests using nox:

.. code:: console

   nox -s xdoctests

Realeasing and Publishing
=========================
This project template provides two major forms of automated publishing

  1. Development 'release' publishes on TestPyPI_
  2. Stable release publishes on PyPI_

Latest deveolpment publishes on TestPyPI
----------------------------------------
Pseudo release a (potentially unstable) development version of your package by
`Pushing <Push_>`_ or `Merging <Merge_>`_ a Pull-Request_ to your
**remote develop branch**. This automatically triggers the *TestPyPI* Workflow_
in :file:`.github/workflows/test-pypi`, which publishes a development version
on TestPyPI_.

To enable your repo interacting with your TestPyPI_ account you need to create an
API-Token_ named ``TEST_PYPI_TOKEN`` in your TestPyPI_
account settings and declare it a Secret_ in your remote Github_ repo.

Assuming you've successfully generated and declared your Secret_ TestPyPI_
Api-Token_, following workflow is proposed for creating a new (unstable)
development release:

  1. Add all changes to your **local develop branch**
  2. Run the full test and lint suite using :code:`nox`.
  3. Commit_ and Push_ your changes to the **remote develop branch**.
  4. The *TestPyPI* Workflow_ in :file:`.github/workflows/test-pypi.yml` automatically
     publishes the package using Poetry_ using a dev versioning scheme.

Stable releases and publishes on PyPI
-------------------------------------

Release a stable version of your package by creating a Release_ of your **main**/
**master** branch via the Github_ website. This triggers the github Workflow_
called PyPI_ residing in :file:`.github/workflows/pypi.yml`, which automatically
creates a release on PyPI_.

To enable your repo interacting with your PyPI_
account you need to create an API-Token_ named ``PYPI_TOKEN`` in your PyPI_
account settings and declare it a Secret_ in your remote Github_ repo.

Assuming you've successfully generated and declared your Secret_ PyPI_
Api-Token_, following workflow is proposed for creating a new release:

  1. Bump the package version on your **local develop branch** using
     :code:`poetry version major|minor|patch|` following the Semantic-Versioning_.
  2. Run the full test and lint suite using :code:`nox`.
  3. Commit_ and Push_ your changes to the **remote develop branch**.
  4. Create a Pull-Request_ from your **remote develop branch** to the
     **remote main** / **master** branch via your remote repo's github webpage.
  5. Merge_ the Pull-Request_ on your remote repo using the github webpage
  6. Create a Release_ using the remote repos webpage.

     Note that the *Release Drafter* Workflow_ in
     :file:`.github/workflows/release-drafter.yml` automatically creates a
     release draft listing all your changes.

  7. The *PyPI* Workflow_ in :file:`.github/workflows/pypi.yml` automatically
     publishes the package using Poetry_


Managing Dependencies
=====================
Project dependencies are managed using Poetry_.

Adding
------

Adding third party dependencies is done by using the :code:`poetry add` command.

poetry add PACKAGE -- Adding required dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add_ a required third party package to your package by using poetry:

.. code:: console

   poetry add PACKAGE

poetry add \-\-dev PACKAGE ^^ Adding additional developer dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add_ additional developer dependencies by using one of the following poetry
commands:

.. code:: console

   poetry add --dev PACKAGE

   poetry add package^1.0
   poetry add "package>=1.0"
   poetry add tessif@latest
   poetry add git+https://github.com/tZ3ma/tessif.git
   poetry add git+https://github.com/tZ3ma/tessif.git#develop
   poetry add ./my-package/

Adding local dependencies in editable mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modify the :file:`pyproject.toml` file inside this project's root directory:

.. code:: console

   [tool.poetry.dependencies]
   my-package = {path = "../my/path", develop = true}

Adding extras/optional dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the package(s) you want to install provide extras, you can specify them when
adding the package by using one of the following lines:

.. code:: console

   poetry add requests[security,socks]
   poetry add "requests[security,socks]~=2.22.0"
   poetry add "git+https://github.com/pallets/flask.git@1.1.1[dotenv,dev]"

Updating
--------
Updating third party dependencies is done by using the :code:`poetry add` command.

nox update -- Updating all dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Update all project dependencies by using:

.. code:: console

   poetry update


nox update package1 package 2 -- Updating explicit dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Update specific dependencies by using:

.. code:: console

   poetry update package1 pakage2

Versioning
----------
Bumping your package's verion is done by using the :code:`poetry version semver`
command. Where semver_ is one of poetry's supported Semantic-Versioning_
specifiers.

poetry version -- Bump yout package version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To bump your package's version use one of the following poetry commands:

.. code:: console

   poetry add patch
   poetry add minor
   poetry add major
   poetry add prepatch
   poetry add preminor
   poetry add premajor
   poetry add prerelease

Removing
--------
Removing third party dependencies is done by using the :code:`poetry remove` command.

poetry remove -- Remove third party dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Remove a required third party package from your package by using poetry:

.. code:: console

   poetry remove PACKAGE

.. Links:

.. _Add: https://python-poetry.org/docs/cli/#add
.. _API-Token: https://pypi.org/help/#apitoken

.. _cj: https://github.com/cjolowicz
.. _Commit: https://docs.github.com/en/rest/commits

.. _darglint: https://github.com/terrencepreilly/darglint
.. _docstrings: https://peps.python.org/pep-0257/#what-is-a-docstring
.. _doctests: https://docs.python.org/3/library/doctest.html

.. _flake8-docstrings: https://gitlab.com/pycqa/flake8-docstrings

.. _Github: https://github.com/

.. _Hypermodern-Python: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/

.. _Merge: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request

.. _Nox: https://nox.thea.codes/
.. _NumPy Style: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy

.. _pip: https://pip.pypa.io/
.. _Poetry: https://python-poetry.org/
.. _Pull-Request: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
.. _Push: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository
.. _PyPI: https://pypi.org/
.. _pytest: https://docs.pytest.org/en/latest/

.. _Release: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

.. _Secret: https://docs.github.com/en/github-ae@latest/actions/security-guides/encrypted-secrets
.. _Semantic-Versioning: https://semver.org/
.. _semver: https://python-poetry.org/docs/cli/#version
.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. _TestPyPI: https://test.pypi.org/

.. _unittests: https://docs.python.org/3/library/unittest.html

.. _Workflow: https://docs.github.com/en/actions/using-workflows/worklow-syntax-for-github-actions

.. _xdoctest: https://github.com/Erotemic/xdoctest
