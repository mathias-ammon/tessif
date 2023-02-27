.. _secondary_constraints:

Secondary Constraints/Objectives
================================

:mod:`Tessif <tessif>` allows defining secondary objectives. For example, constraining global emissions to below a certain threshold.

This is archieved by using the :class:`system model's <tessif.system_model.AbstractEnergySystem>` :paramref:`~tessif.system_model.AbstractEnergySystem.global_constraints` parameter. Which allows to formulate any number of global constraints. However, the only one currently utilized in tessif's plugins is the ``emssions`` keyword, limiting the overall global emissions:

  >>> from tessif_examples import basic
  >>> tessif_sys_mod = basic.create_emission_objective()
  >>> print(tessif_es.global_constraints)
  {'emissions': 60}
