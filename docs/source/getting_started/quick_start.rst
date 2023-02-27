.. _quick_start:

Quick Start
===========

Prior to optimizing a tessif system model using a plugin, you need to
:ref:`install/initialize <init>` the respective plugin.

.. code::

   from tessif_examples import basic
   from tessif import tropp

   PLUGINS = [
       "tessif-oemof-4-4",
       "tessif-pypsa-0-19-3",
       "tessif-fine-2-2-2",
       "tessif-calliope-0-6-6post1",
   ]

   tessif_system_model = basic.create_mwe()

   # ------------ Using Tessif's System Model Tropp ------------------#
   results = tessif_system_model.tropp(
       plugins=PLUGINS,
       # quiet=True,
   )
