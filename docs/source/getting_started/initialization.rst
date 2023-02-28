.. _init:

Tessif Initialization
=====================
Initialize Tessif's main working directory via its command line interface:

.. code-block:: console

   $ tessif init

This creates Tessif's main directory at :file:`~/.tessif./'.

Plugin Integration
==================

Plugin integration can be done in two ways.

Command Line Interface
----------------------
Integrate a supported tessif pluging using tessif's cli for convenience.
For initializing the tessif plugin ``tessif-pypsa-0-19-3`` just use the
command:

.. code-block:: console

   $ tessif integrate tessif-pypsa-0-19-3

This will add a :file:`~/.tessif.d/plugin-venvs/tessif-pypsa-0-19-3/' folder
hosting the ``venv`` required.

The plugins currently suited for this are:

    - tessif-oemof
    - tessif-pypsa

Manual Integration
------------------
In case the automated integration fails, or you wish to install the plugins
manually. Create a the ``venv`` environment for the plugin manually at the
required folder. So for ``tessif-fine-2-2-2`` this would be:

.. code-block:: console

   $ python3.8 -m venv ~/.tessif.d/plugin-venvs/tessif-fine-2-2-2
   $ source ~/.tessif.d/plugin-venvs/tessif-fine-2-2-2/bin/activate
   $ pip install -U tessif-fine-2-2-2

This is currently required for:

    tessif-fine-2-2-2
    tessif-calliope-0-6-6post1

since they only support python3.8.

Note that tessif can support different python binaries, since it activates
the respective virtualenvironment before perfroming the plugin specific
transformation, optimization and post-processing. So tessif can be installed
using python 3.10, whereas some plugins can use e.g. 3.8.

If you decide to install tessif using python3.8, however, integration
using :code:`tessif integrate PLUGIN` is available for all plugins.
