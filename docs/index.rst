***************************************************************************************************
**T**\ ransforming **E**\ nergy **S**\ upply **S**\ ystem model\ **I**\ ng **F**\ ramework (tessif)
***************************************************************************************************

Tessif has been developed for unifying various free and open source modelling tools designed for analysing energy supply systems considering power heat and mobility.

.. contents:: Contents
   :backlinks: top
   :local:


Installation
============


Install using a console with your virtual environment activated:

Latest Stable Version
---------------------
.. code-block:: console

   $ pip install tesif

Latest Development Version (potentially unstable)
-------------------------------------------------

.. code-block:: console

   $ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tessif

This installs the TestPyPI_ version of tessif while resolving the dependencies on PyPI_.



Development Workflows
=====================


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


.. Links:

.. _API-Token: https://pypi.org/help/#apitoken

.. _Commit: https://docs.github.com/en/rest/commits

.. _Github: https://github.com/

.. _Merge: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request

.. _pip: https://pip.pypa.io/
.. _Poetry: https://python-poetry.org/
.. _Pull-Request: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
.. _Push: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository
.. _PyPI: https://pypi.org/


.. _Release: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

.. _Secret: https://docs.github.com/en/github-ae@latest/actions/security-guides/encrypted-secrets
.. _Semantic-Versioning: https://semver.org/

.. _TestPyPI: https://test.pypi.org/


.. _Workflow: https://docs.github.com/en/actions/using-workflows/worklow-syntax-for-github-actions
