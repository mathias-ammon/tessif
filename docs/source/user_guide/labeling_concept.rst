.. _Labeling_Concept:

****************
Labeling Concept
****************
:mod:`Tessif <tessif>` persues a quite unique approach when it comes to naming or labeling its system model components. Following sections provide details on how component labeling is implemented in :mod:`tessif` and how it's features allow both, simple and comprehensive identification as well as  aggregation of auxilliary information.

.. contents:: Contents
   :local:
   :backlinks: top

Bases
*****

Each component that is part of an energy system modeled with the help of tessif must be uniquely identifiable. This is archieved by using :attr:`unique identifiers (uids) <tessif.frused.namedtuples.Uid>`.

Apart from a :paramref:`~tessif.frused.namedtuples.Uid.name` attribute which is mandatory, a :mod:`uid <tessif.frused.namedtuples.Uid>` incorporates several other optional :ref:`parameters <Namedtuples_UidComponents>` storing for example geographical infromation like :paramref:`~tessif.frused.namedtuples.Uid.latitude` or :paramref:`~tessif.frused.namedtuples.Uid.longitude` as well as simulative meta data like :paramref:`~tessif.frused.namedtuples.Uid.node_type`.

Following statement serves as baseline for a component to qualify as unique:

.. warning::
   For a component to be unique the overall combination of it's internally used :ref:`parameters <Namedtuples_UidComponents>` must be unique.

Internal Representation
***********************
Each of tessif component has a :attr:`~tessif.model.components.AbstractEsComponent.uid` with a complete set of parameters. This however does not mean every single one of those parameters is used internally for identification. In fact by default, only the :paramref:`~tessif.frused.namedtuples.Uid.name` is used.

The :mod:`configuration <tessif.frused.configurations>` parameters :attr:`~tessif.frused.configurations.node_uid_style` and :attr:`~tessif.frused.configurations.node_uid_seperator` determine which parts of the :attr:`~tessif.model.components.AbstractEsComponent.uid` are used for internal representation. And can be modified as in the example shown below


Example
*******

  1. Import the configurations module for modifying its attributes:

     >>> import tessif.frused.configurations as configurations

  2. Import and create a minimum working example using tessif-examples:

     >>> from tessif_examples.basic import create_mwe
     >>> example_sys_mod = create_mwe()

  3. Check the current label settings:

     >>> print(configurations.node_uid_style)
     name
     >>> print(configurations.node_uid_seperator)
     _

  4. Print the busses' :class:`uids <tessif.frused.namedtuples.Uid>`:

     >>> for bus in example_sys_mod.busses:
     ...     print(bus.uid)
     Pipeline
     Powerline

  5. Check the :attr:`available settings <tessif.frused.namedtuples.node_uid_styles>` for modifying the
     :attr:`~tessif.frused.configurations.node_uid_style`:

     >>> from tessif.frused.namedtuples import node_uid_styles
     >>> for option in node_uid_styles:
     ...     print(option)
     name
     qualname
     coords
     region
     sector
     carrier
     component
     node_type

  6. Modify the label settings to use geospatial coordinates for the internal representation as well:

     >>> configurations.node_uid_style = 'coords'

  7. Print the busses' :class:`uids <tessif.frused.namedtuples.Uid>` again:

     >>> for bus in example_sys_mod.busses:
     ...     print(bus.uid)
     Pipeline_0.0_0.0
     Powerline_0.0_0.0

  8. Modify the seperator to modify the displayed representation:

     >>> configurations.node_uid_seperator = '_(^0_0^)_'

  9. Print the busses' :class:`uids <tessif.frused.namedtuples.Uid>` again:

     >>> for bus in example_sys_mod.busses:
     ...     print(bus.uid)
     Pipeline_(^0_0^)_0.0_(^0_0^)_0.0
     Powerline_(^0_0^)_0.0_(^0_0^)_0.0

  10. Reset everything back to default:

      >>> configurations.node_uid_style = 'name'
      >>> configurations.node_uid_seperator = '_'


Expansion
*********
To expand :mod:`tessif's <tessif>` labeling concept following 3 stept are recommonded:

   1. Add your parameter to the class body of :class:`tessif.frused.namedtuples.UidBase` as in::

        my_parameter: str

   2. Add your parameter to the ``__new__`` and ``super()`` call of :class:`tessif.frused.namedtuples.Uid` as in:

      - ``__new__``::

           def __new__(cls, ..., my_parameter=default_value)


      - ``super()``::

           self = super(cls,..., my_parameter)

   3. Modify :attr:`tessif.frused.namedtuples.node_uid_styles` to respect the new parameter as for example in::

         node_uid_styles = {
             'name': ['name'],
             'qualname': [i for i in Uid.__new__.__code__.co_varnames
                 if i not in ['self', 'cls']],
              ...
             'my_parameter: ['name', 'my_parameter'],}

Valuation
*********
Realising a dynamic labeling concept involves several advantages and disadvantages of which the most predominant are listed in the following section. The comparisons drawn are to be interpreted as relative to a static labeling concept in which it's up to the user to enforce unique hashable ids for each of the components.

Disadvantages
=============

- Using a :class:`~typing.NamedTuple` instead of a plain string can involve overhead in computational ressources and memory used
- It is more complex for beginners to understand
- Potentially not all of the supported plugins will be able to use such an approach


Advantages
==========

- Utilized label information can adapt to the complexity and size of the modelling task
- Relatively simple expansion / modification
- Individual information can be attached to the components without impacting the system model or the solver
