.. _installation:

Installation
************

Following Sections provide overview on how to install the package.

.. contents:: Contents
   :backlinks: top
   :local:


Standard
========

Linux
-----

Install using a console with your virtual environment activated:

Latest Stable Version
^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

   $ pip install tessif

Latest Development Version (potentially unstable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tessif

This installs the TestPyPI_ version of tessif while resolving the dependencies on PyPI_.


Development
===========

Use the following advice to install the developer version of this package.

Linux
-----

1. You need Python 3.8+ (Pyenv_ is hightly recommended for multiple verions)
2. Install Poetry_ and Nox_
3. Clone the repo to a local directory (uses package name if square bracket
   part is omitted):

   .. code-block:: console

      $ git clone https://github.com/tZ3ma/tessif [tessif-develop]

4. Install the package with development requirements:

   .. code:: console

      $ poetry install

5. Auto generate and activate a virtual environment where the installed package
   is installed:

   .. code:: console

      $ poetry shell

6. (Optional) Alternatively, you can now run an interactive Python session, or
   the command-line interface:

   .. code:: console

      $ poetry run python
      $ poetry run tessif


.. _PyPI: https://pypi.org/
.. _TestPyPI: https://test.pypi.org/
.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/
.. _Pyenv: https://github.com/pyenv/pyenv
