# tessif/model/components.py
"""Tessif component library.

:mod:`~tessif.model.components` is a :mod:`tessif` module
transforming the abstract data representation of an energy system stored as
`mapping
<https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_ into a
'class-instance' like structure.

Mapping like representations are usually returned by utilities part of the
:mod:`~tessif.parse` module.

Note
----
Tessif's energy system model components are deliberately (somewhat) redundant
from a computer science point of view. They are designed to be intuitively used
by engineers. Hence parameters, attributes and namespaces are aggregated in a
way an engineer would classify such components. For more on that see
:mod:`tessif.model`.
"""
import numpy as np
import tessif.frused.namedtuples as nts
from tessif.frused.defaults import energy_system_nodes as es_defaults


class AbstractEsComponent:
    r"""
    Entities only concerned with their unique hashable identifier.

    If it quacks like an AbstractEsComponent, if it walks like an
    AbstractEsComponent it is an AbstractEsComponent.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.name<tessif.frused.namedtuples.Uid.name>`

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with
    :paramref:`~AbstractEsComponent.name` form a
    :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)
    """

    def __init__(self, name, *args, **kwargs):

        # modify this dict to add additional parameters
        kwargs_and_defaults = dict([
            ('name', name),
            ('latitude', kwargs.get('latitude', es_defaults['latitude'])),
            ('longitude', kwargs.get('longitude', es_defaults['longitude'])),
            ('region', kwargs.get('region', es_defaults['region'])),
            ('sector', kwargs.get('sector', es_defaults['sector'])),
            ('carrier', kwargs.get('carrier', es_defaults['carrier'])),
            ('component', kwargs.get('component', es_defaults['component'])),
            ('node_type', kwargs.get('node_type', es_defaults['node_type'])),
        ])

        self._uid = nts.Uid(**kwargs_and_defaults)

        # key parsing functionality wrapper to parameterize the component
        self._parse_arguments(**kwargs)

    def duplicate(self, prefix='', separator='_', suffix='copy'):
        """
        Duplicate the energy system component and return it. Potentially
        modifying it's :paramref:`~AbstractEsComponent.name`.

        Parameters
        ----------
        prefix: str, default=''
           String added to the beginning of the component's
           :paramref:`~AbstractEsComponent.name`, separated by
           :paramref:`~duplicate.separator`.

        separator: str, default='_'
           String used for adding the :paramref:`~duplicate.prefix` and the
           :paramref:`~duplicate.suffix` to the component's
           :paramref:`~AbstractEsComponent.name`.

        suffix: str, default=''
           String added to the beginning of the component's
           :paramref:`~AbstractEsComponent.name`, separated by
           :paramref:`~duplicate.separator`.
        """
        new_attributes = self.attributes
        # get the old uid and transform it into a dict
        new_uid = new_attributes.pop('uid')._asdict()

        # modify the uid's name according to request
        if prefix:
            new_uid['name'] = separator.join([prefix, new_uid['name']])
        if suffix:
            new_uid['name'] = separator.join([new_uid['name'], suffix])

        # create a new component instance using the from_attributes method
        return self.from_attributes(
            attributes={**new_uid, **new_attributes}
        )

    @classmethod
    def from_attributes(cls, attributes):
        """
        Create an :class:`AbstractEsComponent` object from a dictionary
        of :attr:`~AbstractEsComponent.attributes`.
        """
        return cls(**attributes)

    def _parse_arguments_as_singular_values(self, **arguments):
        """Utility for parsing key word arguments in to the form of::

            parameter = value

        Used for parameters like:

            - :attr:`Source.initial_status`
            - :attr:`Storage.initial_soc`
            - ...

        Designed to internally set the energy system components
        parameters. Called by :meth:`_parse_arguments`.
        """
        for parameter, default_value in self._parameters_and_defaults[
                'singular_values'].items():
            setattr(self, '_{}'.format(parameter),
                    arguments.get(parameter, default_value))

    def _parse_arguments_as_singular_value_mappings(self, **arguments):
        """Utility for parsing key word arguments in to the form of::

            parameter = {input/output_string: value}

        Used for parameters like:

            - :attr:`Sink.flow_costs`
            - :attr:`Transformer.flow_emissions`
            - ...

        Designed to internally set the energy system components
        parameters. Called by :meth:`_parse_arguments`.
        """
        for parameter, default_mapping in self._parameters_and_defaults[
                'singular_value_mappings'].items():

            mapping = arguments.get(parameter, default_mapping)
            # reading in data sets from external data can lead to NaN values
            if mapping is np.nan:
                mapping = default_mapping
            setattr(self, '_{}'.format(parameter),
                    {key: mapping[key] for key in sorted(mapping.keys())})

    def _parse_arguments_as_namedtuples(self, **arguments):
        """Utility for parsing key word arguments in to the form of::

            parameter = namedtuple(*values)

        Used for parameters like:

            - :attr:`Transformer.status_inertia`
            - :attr:'Storage.number_of_status_changes`
            - ...

        Designed to internally set the energy system components
        parameters. Called by :meth:`_parse_arguments`.
        """
        for ntple, parameters in self._parameters_and_defaults[
                'namedtuples'].items():
            for parameter, default_tuple in parameters.items():
                tpl = arguments.get(parameter, default_tuple)

                # reading in data sets from external data can lead to NaNs
                if tpl is np.nan:
                    tpl = default_tuple

                setattr(self, '_{}'.format(parameter),
                        getattr(nts, ntple)(*tpl))

    def _parse_arguments_as_mapped_namedtuples(self, **arguments):
        """Utility for parsing key word arguments in to the form of::

            parameter = {input/output_string: namedtuple(*values)}

        Used for parameters like:

            - :attr:`Source.flow_gradients`
            - :attr:`Sink.gradient_costs`
            - :attr:`Transformer.expansion_limits`
            - :attr:'Storage.flow_rates`
            - :attr:`Sink.accumulated_amounts`
            - ...

        Designed to internally set the energy system components
        parameters. Called by :meth:`_parse_arguments`.
        """
        for ntple, parameters in self._parameters_and_defaults[
                'mapped_namedtuples'].items():
            for parameter, default_mapping in parameters.items():
                mapping = arguments.get(parameter, default_mapping)

                # reading in data sets from external data can lead to NaNs
                if mapping is np.nan:
                    mapping = default_mapping

                setattr(self, '_{}'.format(parameter),
                        {key: getattr(nts, ntple)(*mapping[key])
                         for key in sorted(mapping.keys())})

    def _parse_timeseries(self, **arguments):
        """Utility for parsing the key word argument timeseries::

            timeseries = None
            timeseries = {input/output_string: MinMax namedtuple}
        """
        timeseries = arguments.get(
            'timeseries',
            self._parameters_and_defaults.get(
                'timeseries', es_defaults['timeseries']))

        # reading in data sets from external data can lead to NaN values
        if timeseries is np.nan:
            timeseries = self._parameters_and_defaults.get(
                'timeseries', es_defaults['timeseries'])

        # enforce min max tuple:
        if timeseries is not None:
            for interface, tple in timeseries.copy().items():
                timeseries[interface] = nts.MinMax(*tple)

        setattr(self, '_{}'.format('timeseries'), timeseries)

    def _parse_arguments(self, **arguments):
        """
        Key functionality wrapper for parsing component parameters.

        Add new functionalities to expand the support of different kind
        of arguments.

        Parameters
        -----------
        kwargs:
            Key word arguments representing the component's parameters. The
            arguments are provided by the user and filtered by the instance
            variables
        """
        self._parse_arguments_as_singular_values(**arguments)
        self._parse_arguments_as_singular_value_mappings(**arguments)
        self._parse_arguments_as_namedtuples(**arguments)
        self._parse_arguments_as_mapped_namedtuples(**arguments)
        self._parse_timeseries(**arguments)

    def __repr__(self):
        """
        Returns
        -------
        descriptive_string: str
            Returns::

                tsf.Component(attribute_name=attribute, ....)
        """
        return '{!s}('.format(self.__class__) + ', '.join([
            *['{!r}={!r}'.format(
                k.lstrip('_'), v) for k, v in sorted(self.__dict__.items())
              if k != '_parameters_and_defaults'],
            ')',
        ])

    def __str__(self):
        """
        Returns
        -------
        descriptive_string: str
            Returns::

                tsf.Component(
                    attribute_name=attribute
                    ....
                )
        """
        return '{!s}(\n'.format(self.__class__) + ',\n'.join([
            *['    {!r}={!r}'.format(
                k.lstrip('_'), v) for k, v in sorted(self.__dict__.items())
              if k != '_parameters_and_defaults'],
            ')'
        ])

    @property
    def attributes(self):
        """:class:`~collections.abc.Mapping` of entity's energy system
        component attribute names to its respective attribute values.
        """
        return {k.lstrip('_'): v for k, v in sorted(self.__dict__.items())
                if k != '_parameters_and_defaults'}

    @property
    def interfaces(self):
        """:class:`frozenset` holding the component's in- and outputs.
        """
        return self._interfaces

    @property
    def parameters(self):
        """ :class:`~collections.abc.Mapping` of the entity's parameter names
        to its respective values.

        Note
        ----
        Redundant to :attr:`~AbstractEsComponent.attributes`.
        Interface designed for engineers since they would call these values
        ``parameters``, whereas in python ``attributes`` would be the more
        accurate terminology.
        """
        return self.attributes

    @property
    def uid(self):
        """
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as a `hashable
        <https://docs.python.org/3/library/collections.abc.html#collections.abc.Hashable>`_
        unique identifier.
        """
        return self._uid


class Bus(AbstractEsComponent):
    r"""
    Entities only concerned with input and output names.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    inputs: ~collections.abc.Iterable
        An iterable of str(
        :paramref:`AbstractEsComponent.uid<AbstractEsComponent.uid>`).output/
        input strings specifying the bus-entity's inputs.
        e.g.::

            ['node1.electricity', 'node2.electricity',]

        Note
        ----
        Take a look at :attr:`tessif.frused.namedtuples.Uid` as well as
        :attr:`~tessif.frused.configurations.node_uid_style` and
        :attr:`node_uid_styles` for more details on the uid's string
        representation. Especially when having issues with non-unique uid
        solver issues.

    outputs: ~collections.abc.Iterable
        An iterable of str(
        :paramref:`AbstractEsComponent.uid<AbstractEsComponent.uid>`).output/
        input strings specifying the bus-entity's inputs.
        e.g.::

            ['node1.electricity', 'node2.electricity',]

        Note
        ----
        Take a look at :attr:`tessif.frused.namedtuples.Uid` as well as
        :attr:`~tessif.frused.configurations.node_uid_style` and
        :attr:`node_uid_styles` for more details on the uid's string
        representation. Especially when having issues with non-unique uid
        solver issues.

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Bus.name` form an
    id as :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)
    """

    def __init__(self, name, inputs, outputs, *args, **kwargs):
        self._inputs = frozenset(inputs)
        self._outputs = frozenset(outputs)
        self._interfaces = self._inputs.union(self._outputs)

        self._parameters_and_defaults = {
            'singular_values': {
            },
            'singular_value_mappings': {
            },
            'namedtuples': {
            },
            'mapped_namedtuples': {
            },
            'timeseries': es_defaults['timeseries'],
        }
        super().__init__(name, *args, **kwargs)

    @property
    def inputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of str(
        :paramref:`uid<AbstractEsComponent.uid>`).output/input strings
        representing the inputs.
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of str(
        :paramref:`uid<AbstractEsComponent.uid>`).output/input strings
        representing the outputs.
        """
        return self._outputs


class Connector(AbstractEsComponent):
    r"""
    Entities only concerned with connecting 2 busses.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    interfaces: ~collections.abc.Collection
        Collection of length 2 specifying the bus entity's interfaces to
        connect to. Takes the form of (str(:paramref:`Bus.uid`),
        str(:paramref:`Bus.uid`)) e.g.::

            ('my_bus_001', 'my_bus_002')
            ['my_bus_001', 'my_bus_002']

        Note
        ----
        Take a look at :attr:`tessif.frused.namedtuples.Uid` as well as
        :attr:`~tessif.frused.configurations.node_uid_style` and
        :attr:`node_uid_styles` for more details on the uid's string
        representation. Especially when having issues with non-unique uid

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Connector.name` form
    an id as :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)


    Parameters
    ----------
    conversions: ~collections.abc.Mapping
        Mapping of connector relevant (str(input.uid), str(output.uid)) tuples
        to their respective conversion efficiency. With recognized conversion
        efficiencies between 0 and 1 (:math:`\left[0, 1\right]`) e.g.::

            {('bus1', 'bus2'): 0.4,
            ('bus2', 'bus1'): 1,}

        Is interpreted in a way that for 1 quantity flowing from 'bus1' to
        'bus2', 2.5 (1/0.4) quantities are needed. For 1 quantity flowing
        from 'bus2' to 'bus1' on the other hand only 1 quantity is nedded.

    Example
    -------
    Default parameterized :class:`Connector` object:

    >>> from tessif.model.components import Connector
    >>> connector = Connector(name='my_connector',
    ...                       interfaces=('bus_01', 'bus_02'))
    >>> print(connector.uid)
    my_connector

    >>> for k, v in connector.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # Frozensets are transformed to sorted lists for doctesting consistency
    conversions = {('bus_01', 'bus_02'): 1.0, ('bus_02', 'bus_01'): 1.0}
    inputs = ['bus_01', 'bus_02']
    interfaces = ['bus_01', 'bus_02']
    outputs = ['bus_01', 'bus_02']
    timeseries = None
    uid = my_connector
    """

    def __init__(self, name, interfaces, *args, **kwargs):
        self._inputs = frozenset(interfaces)
        self._outputs = frozenset(interfaces)
        self._interfaces = frozenset(interfaces)
        _connections = tuple(interfaces)

        if kwargs.get('conversions', None) is None:
            self._conversions = {
                _connections: es_defaults['efficiency'],
                tuple(reversed(_connections)): es_defaults['efficiency'],
            }
        else:
            self._conversions = kwargs.get('conversions')

        self._parameters_and_defaults = {
            'singular_values': {
            },
            'singular_value_mappings': {
            },
            'namedtuples': {

            },
            'mapped_namedtuples': {
            },
            'timeseries': es_defaults['timeseries'],
        }
        super().__init__(name, *args, **kwargs)

    @property
    def inputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of str(
        :paramref:`uid<Bus.uid>`).output/input strings
        representing the inputs.
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of str(
        :paramref:`uid<Bus.uid>`).output/input strings
        representing the outputs.
        """
        return self._outputs

    @property
    def conversions(self):
        """
        :class:`~collections.abc.Mapping` of connector relevant (input-name,
        output-name) tuples to their respective conversion efficiency. With
        recognized conversion efficiencies between 0 and 1.
        """
        return self._conversions


class Source(AbstractEsComponent):
    r"""
    Entities only concerned with their outputs and related attributes.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    outputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka names
        specifying the source-entity's outputs. e.g.::

            ('fuel',)

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Source.name` form an
    id as :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)

    Parameters
    ----------
    accumulated_amounts: ~collections.abc.Mapping
        Mapping of each :paramref:`output name <Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax`
        :class:`~typing.NamedTuple` describing the minimum/maximum quantity
        the entity's outflow has available (in total).

        Meaning the total sum of a particular outflow happening during the
        simulated time period is less equal than
        :paramref:`~Source.accumulated_amounts` [output_name].max
        and greater equal than :paramref:`~Source.accumulated_amounts`
        [output_name].min

        **Default**::

            {key: MinMax(0, float('+inf')) for key in outputs}

    flow_rates: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.

        **Default**::

            {key: MinMax(0, float('+inf')) for key in outputs}

    flow_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going out this amount of
        cost-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in outputs}

    flow_emissions: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its emission.

        Meaning for each amount per time that is going out this amount of
        emission-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in outputs}

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.

    flow_gradients: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.

        **Default**::

            {k: PositiveNegative(float('+inf'),float('+inf')) for k in outputs}

    gradient_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :paramref:`~Source.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Source.flow_rates` this
        amount of cost-unit is taken into account (by the solver).

        default::

            {k: PositiveNegative(0, 0) for k in outputs}

    timeseries: ~collections.abc.Mapping, default=None
        Mapping an arbitrary number of :paramref:`output names<Source.outputs>`
        to a :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively. For Example

        Setting the maximum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=0, max=np.array([10, 42]))}

        Setting the minimum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=np.array([1, 2]), max=float('+inf'))}

        Fixing the :paramref:`flow_rate <flow_rates>` to a certain timeseries::

            import numpy as np
            timeseries = {input_bus': MinMax(
                min=np.array([1, 2]), max=np.array([1, 2]))}

    expandable: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        boolean variable describing if the mapped
        :paramref:`Source.flow_rates` value can be increased by the
        solver or not.

        **Default**::

            {key: False for key in outputs}

    expansion_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :paramref:`amount per time<Source.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).

        **Default**::

           {key: 0 for key in outputs}

    expansion_limits: ~collections.abc.Mapping
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :paramref:`amount per time<Source.flow_rates>` will be somwhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)

        **Default**::

            {key: MinMax(0, float('+inf')) for key in outputs}


    Note
    ----
    Providing non default parameters for the following set of arguments will
    cause the optimization problem to most likely turn into a
    `Mixed Integer Linear Problem
    <https://en.wikipedia.org/wiki/Integer_programming#Variants>`_

    Parameters
    ----------
    milp: ~collections.abc.Mapping
        Mapping of each :attr:`output name<Source.outputs>` to a boolean
        variable describing if the mapped :attr:`Source.flow_rates` parameter
        can be subject to mixed integer linear constraints.

        **Default**::

            {key: False, for key in outputs}

        warning
        -------
        If :paramref:`~Source.milp` evaluates to ``False`` following set of
        parameters is most likely ignored during optimization.

    initial_status: bool, default=True
        Status variable, indicating if the entity is running, operating,
        working, doing the things its supposed to do, in the beginning
        of the evaluated timeframe.

    status_inertia: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the minimum uptime and downtime.
        With up and downtime describing the minimum amount of following
        discrete timesteps the entity as to be operating or standing stil
        respectively.

        **Default**::

            OnOff(0, 0)

    status_changing_costs: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the cost for changing status
        from ``on`` to ``off`` and from ``off`` to ``on`` respectively

        **Default**::

            OnOff(0, 0)

    number_of_status_changes: ~tessif.frused.namedtuples.OnOff
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.

        **Default**::

            OnOff(float('+inf'), float('+inf'))

    costs_for_being_active: :class:`~number.Number`, default = 0
        Costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).


    Example
    -------
    Default parameterized :class:`Source` object:

    >>> from tessif.model.components import Source
    >>> source = Source(name='my_source', outputs=('fuel',))
    >>> print(source.uid)
    my_source

    >>> print(source.outputs)
    frozenset({'fuel'})

    >>> for k, v in source.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # Frozensets are transformed to sorted lists for doctesting consistency
    accumulated_amounts = {'fuel': MinMax(min=0.0, max=inf)}
    costs_for_being_active = 0.0
    expandable = {'fuel': False}
    expansion_costs = {'fuel': 0.0}
    expansion_limits = {'fuel': MinMax(min=0.0, max=inf)}
    flow_costs = {'fuel': 0.0}
    flow_emissions = {'fuel': 0.0}
    flow_gradients = {'fuel': PositiveNegative(positive=inf, negative=inf)}
    flow_rates = {'fuel': MinMax(min=0.0, max=inf)}
    gradient_costs = {'fuel': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status = 1
    interfaces = ['fuel']
    milp = {'fuel': False}
    number_of_status_changes = OnOff(on=inf, off=inf)
    outputs = ['fuel']
    status_changing_costs = OnOff(on=0.0, off=0.0)
    status_inertia = OnOff(on=0, off=0)
    timeseries = None
    uid = my_source
    """

    def __init__(self, name, outputs, *args, **kwargs):
        self._outputs = frozenset(o for o in outputs)
        self._interfaces = self._outputs

        self._parameters_and_defaults = {
            'singular_values': {
                'initial_status': es_defaults['initial_status'],
                'costs_for_being_active': es_defaults[
                    'costs_for_being_active'],
            },
            'singular_value_mappings': {
                'flow_costs': {key: es_defaults['flow_costs']
                               for key in sorted(self._interfaces)},
                'flow_emissions': {key: es_defaults['emissions']
                                   for key in sorted(self._interfaces)},
                'expandable': {key: es_defaults['expandable']
                               for key in sorted(self._interfaces)},
                'expansion_costs': {key: es_defaults['expansion_costs']
                                    for key in sorted(self._interfaces)},
                'milp': {key: es_defaults['milp']
                         for key in sorted(self._interfaces)},
            },
            'namedtuples': {
                'MinMax': {
                },
                'OnOff': {
                    'status_inertia': nts.OnOff(
                        es_defaults['minimum_uptime'],
                        es_defaults['minimum_downtime']),
                    'status_changing_costs': nts.OnOff(
                        es_defaults['startup_costs'],
                        es_defaults['shutdown_costs']),
                    'number_of_status_changes': nts.OnOff(
                        es_defaults['maximum_startups'],
                        es_defaults['maximum_shutdowns']),
                },
            },
            'mapped_namedtuples': {
                'MinMax': {
                    'expansion_limits': {key: nts.MinMax(
                        es_defaults['minimum_expansion'],
                        es_defaults['maximum_expansion'])
                        for key in sorted(self._interfaces)},
                    'flow_rates': {key: nts.MinMax(
                        es_defaults['minimum_flow_rate'],
                        es_defaults['maximum_flow_rate'])
                        for key in sorted(self._interfaces)},
                    'accumulated_amounts': {key: nts.MinMax(
                        es_defaults['accumulated_minimum'],
                        es_defaults['accumulated_maximum'])
                        for key in sorted(self._interfaces)},
                },
                'PositiveNegative': {
                    'flow_gradients': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient'],
                        es_defaults['negative_gradient'])
                        for key in sorted(self._interfaces)},
                    'gradient_costs': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient_costs'],
                        es_defaults['negative_gradient_costs'])
                        for key in sorted(self._interfaces)},
                },
            }
        }

        super().__init__(name, *args, **kwargs)

    @property
    def outputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of
        hashable unique identifiers. Usually a string aka a name representing
        the outputs.
        """
        return self._outputs

    @property
    def accumulated_amounts(self):
        """:class:`~collections.abc.Mapping`
        of each :paramref:`output name <Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax`
        :class:`~typing.NamedTuple` describing the minimum/maximum quantity
        the entity's outflow has available (in total).

        Meaning the total sum of a particular outflow happening during the
        simulated time period is less equal
        than :paramref:`~Source.accumulated_amounts` [output_name].max and
        greater equal than :paramref:`~Source.accumulated_amounts`
        [output_name].min
        """
        return self._accumulated_amounts

    @property
    def flow_rates(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.
        """
        return self._flow_rates

    @property
    def flow_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going out this amount of
        cost-unit is taken into account (by the solver).
        """
        return self._flow_costs

    @property
    def flow_emissions(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its emissions

        Meaning for each amount per time that is going out this amount of
        emission-unit is taken into account (by the solver).

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.
        """
        return self._flow_emissions

    @property
    def flow_gradients(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.
        """
        return self._flow_gradients

    @property
    def gradient_costs(self):
        """ :class:`~collections.abc.Mapping`
        Mapping of each :paramref:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :attr:`~Source.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Source.flow_rates` this
        amount of cost-unit is taken into account (by the solver).
        """
        return self._gradient_costs

    @property
    def timeseries(self):
        """ :class:`~collections.abc.Mapping` of an arbitrary number
        of :attr:`output names<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively.
        """
        return self._timeseries

    @property
    def expandable(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a boolean variable
        describing if the mapped :attr:`Source.flow_rates` value can be
        increased by the  solver or not.
        """
        return self._expandable

    @property
    def expansion_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :attr:`amount per time<Source.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).
        """
        return self._expansion_costs

    @property
    def expansion_limits(self):
        r""" :class:`~collections.abc.Mapping`
        of each :attr:`output name<Source.outputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :attr:`amount per time<Source.flow_rates>` will be somewhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)
        """
        return self._expansion_limits

    @property
    def initial_status(self):
        """ :class:`Status variable<bool>`, indicating if the entity is
        running, operating, working, doing the things its supposed to do in
        the beginning of the evaluated timeframe.
        """
        return self._initial_status

    @property
    def status_inertia(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the minimum uptime and downtime. With up and downtime
        describing the minimum amount of following discrete timesteps the
        entity as to be operating or standing still respectively.
        """
        return self._status_inertia

    @property
    def status_changing_costs(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the cost for changing status from ``on`` to ``off`` and
        from ``off`` to ``on`` respectively.
        """
        return self._status_changing_costs

    @property
    def number_of_status_changes(self):
        """An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.
        """
        return self._number_of_status_changes

    @property
    def costs_for_being_active(self):
        """ A :class:`~number.Number`, default = 0
        Describing the costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).
        """
        return self._costs_for_being_active


class Sink(AbstractEsComponent):
    r"""
    Entities only concerned with their inputs and related attributes.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    inputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka names
        specifying the source-entity's inputs. e.g.::

            ('fuel',)

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Sink.name` form an id
    as a :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)

    Parameters
    ----------

    accumulated_amounts: ~collections.abc.Mapping
        Mapping of each :paramref:`input name <Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax`
        :class:`~typing.NamedTuple` describing the minimum/maximum quantity
        the entity's inflow has available (in total).

        Meaning the total sum of a particular inflow happening during the
        simulated time period is less equal than
        :paramref:`~Sink.accumulated_amounts` [input_name].max
        and greater equal than :paramref:`~Sink.accumulated_amounts`
        [input_name].min

        **Default**::

            {key: MinMax(0, float('+inf')) for key in inputs}

    flow_rates: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going in during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.

        **Default**::

            {key: MinMax(0, float('+inf')) for key in inputs}

    flow_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going in this amount of
        cost-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in inputs}

    flow_emissions: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its emission.

        Meaning for each amount per time that is going in this amount of
        emission-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in inputs}

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.

    flow_gradients: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.

        **Default**::

            k: PositiveNegative(float('+inf'),float('+inf')) for k in inputs}

    gradient_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :paramref:`~Sink.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Sink.flow_rates` this
        amount of cost-unit is taken into account (by the solver).

        **Default**::

            {k: PositiveNegative(0, 0) for k in inputs}

    timeseries: ~collections.abc.Mapping, default=None
        Mapping an arbitrary number of :paramref:`input names<Sink.inputs>`
        to a :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively. For Example

        Setting the maximum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=0, max=np.array([10, 42]))}

        Setting the minimum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=np.array([1, 2]), max=float('+inf'))}

        Fixing the :paramref:`flow_rate <flow_rates>` to a certain timeseries::

            import numpy as np
            timeseries = {input_bus': MinMax(
                min=np.array([1, 2]), max=np.array([1, 2]))}

    expandable: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        boolean variable describing if the mapped
        :paramref:`Sink.flow_rates` value can be increased by the
        solver or not.

        **Default**::

            {key: False for key in inputs}

    expansion_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :paramref:`amount per time<Sink.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).

        **Default**::

            {key: 0 for key in inputs}

    expansion_limits: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :paramref:`amount per time<Sink.flow_rates>` will be somwhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)

        **Default**::

            {key: MinMax(0, float('+inf')) for key in inputs}


    Note
    ----
    Providing non default parameters for the following set of arguments will
    cause the optimization problem to most likely turn into a
    `Mixed Integer Linear Problem
    <https://en.wikipedia.org/wiki/Integer_programming#Variants>`_

    Parameters
    ----------
    milp: ~collections.abc.Mapping
        Mapping of each :attr:`output name<Sink.inputs>` to a boolean variable
        describing if the mapped :attr:`Sink.flow_rates` parameter can be
        subject to mixed integer linear constraints.

        **Default**::

            {key: False for key in inputs}

        warning
        -------
        If :paramref:`~Sink.milp` evaluates to ``False`` following set of
        parameters is most likely ignored during optimization.

    initial_status: bool, default=True
        Status variable, indicating if the entity is running, operating,
        working, doing the things its supposed to do, in the beginning
        of the evaluated timeframe.

    status_inertia: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the minimum uptime and downtime.
        With up and downtime describing the minimum amount of following
        discrete timesteps the entity as to be operating or standing stil
        respectively.

        **Default**::

            OnOff(0, 0)

    status_changing_costs: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the cost for changing status
        from ``on`` to ``off`` and from ``off`` to ``on`` respectively.

        **Default**::

            OnOff(0, 0)

    number_of_status_changes: ~tessif.frused.namedtuples.OnOff
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.

        **Default**::

            OnOff(float('+inf'), float('+inf'))

    costs_for_being_active: :class:`~number.Number`, default = 0
        Costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).


    Example
    -------
    Default parameterized :class:`Sink` object:

    >>> from tessif.model.components import Sink
    >>> sink = Sink(name='my_sink', inputs=('electricity',))
    >>> print(sink.uid)
    my_sink

    >>> print(sink.inputs)
    frozenset({'electricity'})

    Accessing all its :attr:`~Sink.attributes`:

    >>> for k, v in sink.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # frozensets are transformed to sorted lists for doctesting consistency
    accumulated_amounts = {'electricity': MinMax(min=0.0, max=inf)}
    costs_for_being_active = 0.0
    expandable = {'electricity': False}
    expansion_costs = {'electricity': 0.0}
    expansion_limits = {'electricity': MinMax(min=0.0, max=inf)}
    flow_costs = {'electricity': 0.0}
    flow_emissions = {'electricity': 0.0}
    flow_gradients = {'electricity': PositiveNegative(positive=inf, negative=inf)}
    flow_rates = {'electricity': MinMax(min=0.0, max=inf)}
    gradient_costs = {'electricity': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status = 1
    inputs = ['electricity']
    interfaces = ['electricity']
    milp = {'electricity': False}
    number_of_status_changes = OnOff(on=inf, off=inf)
    status_changing_costs = OnOff(on=0.0, off=0.0)
    status_inertia = OnOff(on=0, off=0)
    timeseries = None
    uid = my_sink
    """

    def __init__(self, name, inputs, *args, **kwargs):
        self._inputs = frozenset(inputs)
        self._interfaces = self._inputs

        # modify this dict for adding additional parameters
        self._parameters_and_defaults = {
            'singular_values': {
                'initial_status': es_defaults['initial_status'],
                'costs_for_being_active': es_defaults[
                    'costs_for_being_active'],
            },
            'singular_value_mappings': {
                'flow_costs': {key: es_defaults['flow_costs']
                               for key in sorted(self._interfaces)},
                'flow_emissions': {key: es_defaults['emissions']
                                   for key in sorted(self._interfaces)},
                'expandable': {key: es_defaults['expandable']
                               for key in sorted(self._interfaces)},
                'expansion_costs': {key: es_defaults['expansion_costs']
                                    for key in sorted(self._interfaces)},
                'milp': {key: es_defaults['milp']
                         for key in sorted(self._interfaces)},
            },
            'namedtuples': {
                'MinMax': {
                },
                'OnOff': {
                    'status_inertia': nts.OnOff(
                        es_defaults['minimum_uptime'],
                        es_defaults['minimum_downtime']),
                    'status_changing_costs': nts.OnOff(
                        es_defaults['startup_costs'],
                        es_defaults['shutdown_costs']),
                    'number_of_status_changes': nts.OnOff(
                        es_defaults['maximum_startups'],
                        es_defaults['maximum_shutdowns']),
                },
            },
            'mapped_namedtuples': {
                'MinMax': {
                    'expansion_limits': {key: nts.MinMax(
                        es_defaults['minimum_expansion'],
                        es_defaults['maximum_expansion'])
                        for key in sorted(self._interfaces)},
                    'flow_rates': {key: nts.MinMax(
                        es_defaults['minimum_flow_rate'],
                        es_defaults['maximum_flow_rate'])
                        for key in sorted(self._interfaces)},
                    'accumulated_amounts': {key: nts.MinMax(
                        es_defaults['accumulated_minimum'],
                        es_defaults['accumulated_maximum'])
                        for key in sorted(self._interfaces)},
                },
                'PositiveNegative': {
                    'flow_gradients': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient'],
                        es_defaults['negative_gradient'])
                        for key in sorted(self._interfaces)},
                    'gradient_costs': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient_costs'],
                        es_defaults['negative_gradient_costs'])
                        for key in sorted(self._interfaces)},
                },
            },
            'timeseries': es_defaults['timeseries'],
        }

        super().__init__(name, *args, **kwargs)

    @property
    def inputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of
        hashable unique identifiers. Usually a string aka a name representing
        the inputs.
        """
        return self._inputs

    @property
    def accumulated_amounts(self):
        """:class:`~collections.abc.Mapping` of each
        :attr:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum/maximum quantity the entity's inflow has available (in total).

        Meaning the total sum of a particular inflow happening during the
        simulated time period is less equal than
        :paramref:`~Sink.accumulated_amounts` [input_name].max
        and greater equal than :paramref:`~Sink.accumulated_amounts`
        [input_name].min
        """
        return self._accumulated_amounts

    @property
    def flow_rates(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going in during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.
        """
        return self._flow_rates

    @property
    def flow_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going in this amount of
        cost-unit is taken into account (by the solver).
        """
        return self._flow_costs

    @property
    def flow_emissions(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its emissions

        Meaning for each amount per time that is going in this amount of
        emission-unit is taken into account (by the solver).

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.
        """
        return self._flow_emissions

    @property
    def flow_gradients(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.
        """
        return self._flow_gradients

    @property
    def gradient_costs(self):
        """ :class:`~collections.abc.Mapping`
        Mapping of each :paramref:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :attr:`~Sink.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Sink.flow_rates` this
        amount of cost-unit is taken into account (by the solver).
        """
        return self._gradient_costs

    @property
    def timeseries(self):
        """ :class:`~collections.abc.Mapping` of an arbitrary number
        of :attr:`input names<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively.
        """
        return self._timeseries

    @property
    def expandable(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a boolean variable
        describing if the mapped :attr:`Sink.flow_rates` value can be
        increased by the  solver or not.
        """
        return self._expandable

    @property
    def expansion_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :attr:`amount per time<Sink.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).
        """
        return self._expansion_costs

    @property
    def expansion_limits(self):
        r""" :class:`~collections.abc.Mapping`
        of each :attr:`input name<Sink.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :attr:`amount per time<Sink.flow_rates>` will be somewhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)
        """
        return self._expansion_limits

    @property
    def initial_status(self):
        """ :class:`Status variable<bool>`, indicating if the entity is
        running, operating, working, doing the things its supposed to do in
        the beginning of the evaluated timeframe.
        """
        return self._initial_status

    @property
    def status_inertia(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the minimum uptime and downtime. With up and downtime
        describing the minimum amount of following discrete timesteps the
        entity as to be operating or standing still respectively.
        """
        return self._status_inertia

    @property
    def status_changing_costs(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the cost for changing status from ``on`` to ``off`` and
        from ``off`` to ``on`` respectively.
        """
        return self._status_changing_costs

    @property
    def number_of_status_changes(self):
        """An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.
        """
        return self._number_of_status_changes

    @property
    def costs_for_being_active(self):
        """ A :class:`~number.Number`, default = 0
        Describing the costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).
        """
        return self._costs_for_being_active


class Transformer(AbstractEsComponent):
    r"""
     Entities only concerned with mapping their inflows to their outflows.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    inputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka
        names specifying the transformer-entity's inputs. e.g.::

            ['fuel_1', 'fuel_2']

    outputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka
        names specifying the transformer-entity's outputs. e.g.::

            ['electricity', 'heat']

    conversions: ~collections.abc.Mapping
        Mapping of transformer relevant (input-name, output-name) tuples to
        their respective conversion efficiency. With recognized conversion
        efficiencies between 0 and 1 (:math:`\left[0, 1\right]`) e.g.::

            {('fuel_1', 'electricity'): 0.4,
            ('fuel_2', 'electricity'): 0.8,}

        Is interpreted in a way that for transforming 1 quantity of
        'electricity' 2.5 quantities (1/0.4)  of 'fuel_1' and 1.25
        quantities (1/0.8) of 'fuel_2' are needed.

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Transformer.name`
    form an id as a :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)

    Parameters
    ----------

    flow_rates: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going in/out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.

        **Default**::

            {key: MinMax(0, float('+inf')) for key in [*inputs, *outputs]}

    flow_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going in/out this amount of
        cost-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

    flow_emissions: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its emission.

        Meaning for each amount per time that is going in/out this amount of
        emission-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.

    flow_gradients: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.

        **Default**::

            {k: PositiveNegative(float('+inf'),float('+inf'))
             for k in [*inputs, *outputs]}

    gradient_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :paramref:`~Transformer.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Transformer.flow_rates` this
        amount of cost-unit is taken into account (by the solver).

        **Default**::

            {k: PositiveNegative(0, 0) for k in [*inputs, *outputs]}

    timeseries: ~collections.abc.Mapping, default=None
        Mapping an arbitrary number of :paramref:`output names<
        Transformer.outputs>` to a :class:`~tessif.frused.namedtuples.MinMax`
        tuple describing the minimum and maximum :paramref:`flow_rates`
        respectively. For Example

        Setting the maximum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=0, max=np.array([10, 42]))}

        Setting the minimum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=np.array([1, 2]), max=float('+inf'))}

        Fixing the :paramref:`flow_rate <flow_rates>` to a certain timeseries::

            import numpy as np
            timeseries = {input_bus': MinMax(
                min=np.array([1, 2]), max=np.array([1, 2]))}

    expandable: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<Transformer.inputs>` to a
        boolean variable describing if the mapped
        :paramref:`Transformer.flow_rates` value can be increased by the
        solver or not.

        **Default**::

            {key: False for key in [*inputs, *outputs]}

    expansion_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :paramref:`amount per time<Transformer.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

    expansion_limits: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :paramref:`amount per time<Transformer.flow_rates>` will be
        somwhere between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)

        **Default**::

            {k: MinMax(0, float('+inf')) for k in [*inputs, *outputs]}


    Note
    ----
    Providing non default parameters for the following set of arguments will
    cause the optimization problem to most likely turn into a
    `Mixed Integer Linear Problem
    <https://en.wikipedia.org/wiki/Integer_programming#Variants>`_

    Parameters
    ----------
    milp: ~collections.abc.Mapping
        Mapping of each :attr:`input/output name <Transfomer.inputs>` to a
        boolean variable describing if the mapped
        :attr:`Transformer.flow_rates` parameter can be
        subject to mixed integer linear constraints.

        **Default**::

            {key: False for key in [*inputs, *outputs]}

    milp: bool, default=False,
        Boolean variable indicating if the component's parameters are to be
        parsed as mixed integer-linear optimization problem or not.

        warning
        -------
        If :paramref:`~Transformer.milp` evaluates to ``False`` following set
        of parameters is most likely ignored during optimization.

    initial_status: bool, default=True
        Status variable, indicating if the entity is running, operating,
        working, doing the things its supposed to do, in the beginning
        of the evaluated timeframe.

    status_inertia: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the minimum uptime and downtime.
        With up and downtime describing the minimum amount of following
        discrete timesteps the entity as to be operating or standing stil
        respectively.

        **Default**::

            OnOff(0, 0)

    status_changing_costs: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the cost for changing status
        from ``on`` to ``off`` and from ``off`` to ``on`` respectively

        **Default**::

            OnOff(0, 0)

    number_of_status_changes: ~tessif.frused.namedtuples.OnOff
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.

        **Default**::

            OnOff(float('+inf'), float('+inf'))

    costs_for_being_active: :class:`~number.Number`, default = 0
        Costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).

    Example
    -------
    Default parameterized :class:`Transformer` object:

    >>> import pprint
    >>> from tessif.model.components import Transformer
    >>> transformer = Transformer(
    ...     name='my_transformer', inputs=('fuel',), outputs=('electricity',),
    ...     conversions={('fuel', 'electricity'): 0.42})
    >>> print(transformer.uid)
    my_transformer

    >>> print(transformer.inputs)
    frozenset({'fuel'})

    >>> print(transformer.outputs)
    frozenset({'electricity'})

    >>> print(sorted(transformer.interfaces))
    ['electricity', 'fuel']

    Accessing all its :attr:`~Transformer.attributes`:

    >>> for k, v in transformer.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # frozensets are sorted for consistent doctesting
    conversions = {('fuel', 'electricity'): 0.42}
    costs_for_being_active = 0.0
    expandable = {'electricity': False, 'fuel': False}
    expansion_costs = {'electricity': 0.0, 'fuel': 0.0}
    expansion_limits = {'electricity': MinMax(min=0.0, max=inf), 'fuel': MinMax(min=0.0, max=inf)}
    flow_costs = {'electricity': 0.0, 'fuel': 0.0}
    flow_emissions = {'electricity': 0.0, 'fuel': 0.0}
    flow_gradients = {'electricity': PositiveNegative(positive=inf, negative=inf), 'fuel': PositiveNegative(positive=inf, negative=inf)}
    flow_rates = {'electricity': MinMax(min=0.0, max=inf), 'fuel': MinMax(min=0.0, max=inf)}
    gradient_costs = {'electricity': PositiveNegative(positive=0.0, negative=0.0), 'fuel': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status = 1
    inputs = ['fuel']
    interfaces = ['electricity', 'fuel']
    milp = {'electricity': False, 'fuel': False}
    number_of_status_changes = OnOff(on=inf, off=inf)
    outputs = ['electricity']
    status_changing_costs = OnOff(on=0.0, off=0.0)
    status_inertia = OnOff(on=0, off=0)
    timeseries = None
    uid = my_transformer
    """

    def __init__(self, name, inputs, outputs, conversions, *args, **kwargs):
        self._inputs = frozenset(i for i in inputs)
        self._outputs = frozenset(o for o in outputs)
        self._interfaces = self._inputs.union(self._outputs)
        self._conversions = conversions

        self._parameters_and_defaults = {
            'singular_values': {
                'initial_status': es_defaults['initial_status'],
                'costs_for_being_active': es_defaults[
                    'costs_for_being_active'],
            },
            'singular_value_mappings': {
                'flow_costs': {key: es_defaults['flow_costs']
                               for key in sorted(self._interfaces)},
                'flow_emissions': {key: es_defaults['emissions']
                                   for key in sorted(self._interfaces)},
                'expandable': {key: es_defaults['expandable']
                               for key in sorted(self._interfaces)},
                'expansion_costs': {key: es_defaults['expansion_costs']
                                    for key in sorted(self._interfaces)},
                'milp': {key: es_defaults['milp']
                         for key in sorted(self._interfaces)},
            },
            'namedtuples': {
                'MinMax': {
                },
                'OnOff': {
                    'status_inertia': nts.OnOff(
                        es_defaults['minimum_uptime'],
                        es_defaults['minimum_downtime']),
                    'status_changing_costs': nts.OnOff(
                        es_defaults['startup_costs'],
                        es_defaults['shutdown_costs']),
                    'number_of_status_changes': nts.OnOff(
                        es_defaults['maximum_startups'],
                        es_defaults['maximum_shutdowns']),
                },
            },
            'mapped_namedtuples': {
                'MinMax': {
                    'expansion_limits': {key: nts.MinMax(
                        es_defaults['minimum_expansion'],
                        es_defaults['maximum_expansion'])
                        for key in sorted(self._interfaces)},
                    'flow_rates': {key: nts.MinMax(
                        es_defaults['minimum_flow_rate'],
                        es_defaults['maximum_flow_rate'])
                        for key in sorted(self._interfaces)},
                },
                'PositiveNegative': {
                    'flow_gradients': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient'],
                        es_defaults['negative_gradient'])
                        for key in sorted(self._interfaces)},
                    'gradient_costs': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient_costs'],
                        es_defaults['negative_gradient_costs'])
                        for key in sorted(self._interfaces)},
                },
            },
            'timeseries': es_defaults['timeseries'],
        }

        super().__init__(name, *args, **kwargs)

    @property
    def inputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of
        hashable unique identifiers. Usually a string aka a name representing
        the inputs.
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :class:`Hashable<collections.abc.Hashable>` container of
        hashable unique identifiers. Usually a string aka a name representing
        the outputs.
        """
        return self._outputs

    @property
    def conversions(self):
        r""" :class:`~collections.abc.Mapping` of transformer relevant
        (inflow-name, outflow-name) tuples to their respective conversion
        efficiency. With recognized conversion  efficiencies between 0 and 1
        (:math:`\left[0, 1\right]`)
        """
        return self._conversions

    @property
    def flow_rates(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.
        """
        return self._flow_rates

    @property
    def flow_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going out this amount of
        cost-unit is taken into account (by the solver).
        """
        return self._flow_costs

    @property
    def flow_emissions(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its emissions

        Meaning for each amount per time that is going out this amount of
        emission-unit is taken into account (by the solver).

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.
        """
        return self._flow_emissions

    @property
    def flow_gradients(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.
        """
        return self._flow_gradients

    @property
    def gradient_costs(self):
        """ :class:`~collections.abc.Mapping`
        Mapping of each :paramref:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :attr:`~Transformer.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Transformer.flow_rates` this
        amount of cost-unit is taken into account (by the solver).
        """
        return self._gradient_costs

    @property
    def timeseries(self):
        """ :class:`~collections.abc.Mapping` of an arbitrary number
        of :attr:`input/output names<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively.
        """
        return self._timeseries

    @property
    def expandable(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a boolean
        variable describing if the mapped :attr:`Transformer.flow_rates`
        value can be increased by the  solver or not.
        """
        return self._expandable

    @property
    def expansion_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :attr:`amount per time<Transformer.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).
        """
        return self._expansion_costs

    @property
    def expansion_limits(self):
        r""" :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Transformer.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :attr:`amount per time<Transformer.flow_rates>` will be somewhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)
        """
        return self._expansion_limits

    @property
    def initial_status(self):
        """ :class:`Status variable<bool>`, indicating if the entity is
        running, operating, working, doing the things its supposed to do in
        the beginning of the evaluated timeframe.
        """
        return self._initial_status

    @property
    def status_inertia(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the minimum uptime and downtime. With up and downtime
        describing the minimum amount of following discrete timesteps the
        entity as to be operating or standing still respectively.
        """
        return self._status_inertia

    @property
    def status_changing_costs(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the cost for changing status from ``on`` to ``off`` and
        from ``off`` to ``on`` respectively.
        """
        return self._status_changing_costs

    @property
    def number_of_status_changes(self):
        """An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.
        """
        return self._number_of_status_changes

    @property
    def costs_for_being_active(self):
        """ A :class:`~number.Number`, default = 0
        Describing the costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).
        """
        return self._costs_for_being_active


class CHP(Transformer):
    r"""Entities that are like Transformers but with additional constraints.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    inputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka
        names specifying the chp-entity's inputs. e.g.::

            ['fuel_1', 'fuel_2']

    outputs: ~collections.abc.Iterable
        An iterable of hashable unique identifiers. Usually strings, aka
        names specifying the chp-entity's outputs. e.g.::

            ['electricity', 'heat']

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforenamed arguments together with :paramref:`~CHP.name`
    form an id as a :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)

    Parameters
    ----------

    back_pressure: bool,
        Boolean to specify if back-pressure characteristics shall be used.
        Set to True and Q_CW_min to zero for back-pressure turbines.

    conversion_factor_full_condensation: ~collections.abc.Mapping
        :class:`~collections.abc.Mapping` where the
        (inflow-name, outflow-name) tuple of the main flow is the only key and
        it's conversion efficiency when there is no tapped flow is it's value.
        Conversion efficiencies are expected to be between 0 and 1
        (:math:`\left[0, 1\right]`).

    el_efficiency_wo_dist_heat: ~tessif.frused.namedtuples.MinMax
        Electric efficiency at min/max fuel flow without district heating.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the efficiency at that timestep.

    enthalpy_loss: ~tessif.frused.namedtuples.MinMax
        Share of flue gas enthalpy loss at min/max heat extraction.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the share of flue gas enthalpy loss for that timestep.

    power_wo_dist_heat: ~tessif.frused.namedtuples.MinMax
        Min/max electric power without district heating.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is the power at that timestep.

    power_loss_index: list
        Marginal loss of electric power for each additional unit of heat.

        Expects a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the marginal loss of power at that timestep.

    min_condenser_load: list
        Minimal thermal condenser load to cooling water.

        Expects a list where the length is the same as the
        number of timesteps and each entry is the minimal condenser load at
        that timestep.

    conversions: ~collections.abc.Mapping
        Mapping of chp relevant (input-name, output-name) tuples to
        their respective conversion efficiency. With recognized conversion
        efficiencies between 0 and 1 (:math:`\left[0, 1\right]`) e.g.::

            {('fuel_1', 'electricity'): 0.4,
            ('fuel_2', 'electricity'): 0.8,}

        Is interpreted in a way that for transforming 1 quantity of
        'electricity' 2.5 quantities (1/0.4)  of 'fuel_1' and 1.25
        quantities (1/0.8) of 'fuel_2' are needed.

        In the CHP class 'conversions' is optional because the efficiencies can
        also be specified with 'el_efficiency_wo_dist_heat' and
        'power_loss_index'. Using both ways to specify the efficiencies at the
        same time might lead to unexpected results.

    flow_rates: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going in/out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.

        In the CHP Class it is also possible to constrain the flow rates with a
        combination of 'power_wo_dist_heat', 'enthalpy_loss',
        'min_condenser_load' and 'power_loss_index'. It should be possible
        to combine those attributes with 'flow_rates' but if problems appear,
        try to leave 'flow_rates' away and change the other attributes in such
        a way that you have the same behvior.

        **Default**::

            {key: MinMax(0, float('+inf')) for key in [*inputs, *outputs]}

    flow_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going in/out this amount of
        cost-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

    flow_emissions: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~numbers.Number` specifying its emission.

        Meaning for each amount per time that is going in/out this amount of
        emission-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.

    flow_gradients: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.

        **Default**::

            {k: PositiveNegative(float('+inf'),float('+inf'))
             for k in [*inputs, *outputs]}

    gradient_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :paramref:`~CHP.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~CHP.flow_rates` this
        amount of cost-unit is taken into account (by the solver).

        **Default**::

            {k: PositiveNegative(0, 0) for k in [*inputs, *outputs]}

    timeseries: ~collections.abc.Mapping, default=None
        Mapping an arbitrary number of :paramref:`output names<
        CHP.outputs>` to a :class:`~tessif.frused.namedtuples.MinMax`
        tuple describing the minimum and maximum :paramref:`flow_rates`
        respectively. For Example

        Setting the maximum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=0, max=np.array([10, 42]))}

        Setting the minimum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=np.array([1, 2]), max=float('+inf'))}

        Fixing the :paramref:`flow_rate <flow_rates>` to a certain timeseries::

            import numpy as np
            timeseries = {input_bus': MinMax(
                min=np.array([1, 2]), max=np.array([1, 2]))}

    expandable: ~collections.abc.Mapping
        Mapping of each :paramref:`input name<CHP.inputs>` to a
        boolean variable describing if the mapped
        :paramref:`CHP.flow_rates` value can be increased by the
        solver or not.

        **Default**::

            {key: False for key in [*inputs, *outputs]}

    expansion_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :paramref:`amount per time<CHP.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).

        **Default**::

            {key: 0 for key in [*inputs, *outputs]}

    expansion_limits: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<CHP.inputs>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :paramref:`amount per time<CHP.flow_rates>` will be
        somewhere between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)

        **Default**::

            {k: MinMax(0, float('+inf')) for k in [*inputs, *outputs]}

    Note
    ----
    Providing non default parameters for the following set of arguments will
    cause the optimization problem to most likely turn into a
    `Mixed Integer Linear Problem
    <https://en.wikipedia.org/wiki/Integer_programming#Variants>`_

    Parameters
    ----------
    milp: ~collections.abc.Mapping
        Mapping of each :attr:`input/output name <CHP.inputs>` to a
        boolean variable describing if the mapped
        :attr:`CHP.flow_rates` parameter can be
        subject to mixed integer linear constraints.

        **Default**::

            {key: False for key in [*inputs, *outputs]}

    milp: bool, default=False,
        Boolean variable indicating if the component's parameters are to be
        parsed as mixed integer-linear optimization problem or not.

        warning
        -------
        If :paramref:`~CHP.milp` evaluates to ``False`` following set
        of parameters is most likely ignored during optimization.

    initial_status: bool, default=True
        Status variable, indicating if the entity is running, operating,
        working, doing the things its supposed to do, in the beginning
        of the evaluated timeframe.

    status_inertia: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the minimum uptime and downtime.
        With up and downtime describing the minimum amount of following
        discrete timesteps the entity as to be operating or standing stil
        respectively.

        **Default**::

            OnOff(0, 0)

    status_changing_costs: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the cost for changing status
        from ``on`` to ``off`` and from ``off`` to ``on`` respectively

        **Default**::

            OnOff(0, 0)

    number_of_status_changes: ~tessif.frused.namedtuples.OnOff
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.

        **Default**::

            OnOff(float('+inf'), float('+inf'))

    costs_for_being_active: :class:`~number.Number`, default = 0
        Costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).

    Example
    -------
    Variable efficiency :class:`CHP` object:

    >>> import pprint
    >>> from tessif.model.components import CHP
    >>> chp = CHP(
    ...     name='my_chp', inputs=('fuel',), outputs=('electricity','heat',),
    ...     conversions={('fuel', 'electricity'): 0.3, ('fuel', 'heat'): 0.5},
    ...     conversion_factor_full_condensation={('fuel', 'electricity'): 0.5})
    >>> print(chp.uid)
    my_chp

    >>> print(chp.inputs)
    frozenset({'fuel'})

    >>> print(sorted(chp.outputs))
    ['electricity', 'heat']

    >>> print(sorted(chp.interfaces))
    ['electricity', 'fuel', 'heat']

    Accessing all its :attr:`~Transformer.attributes`:

    >>> for k, v in chp.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # frozensets are sorted for consistent doctesting
    back_pressure = None
    conversion_factor_full_condensation = {('fuel', 'electricity'): 0.5}
    conversions = {('fuel', 'electricity'): 0.3, ('fuel', 'heat'): 0.5}
    costs_for_being_active = 0.0
    el_efficiency_wo_dist_heat = MinMax(min=None, max=None)
    enthalpy_loss = MinMax(min=None, max=None)
    expandable = {'electricity': False, 'fuel': False, 'heat': False}
    expansion_costs = {'electricity': 0.0, 'fuel': 0.0, 'heat': 0.0}
    expansion_limits = {'electricity': MinMax(min=0.0, max=inf), 'fuel': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0.0, max=inf)}
    flow_costs = {'electricity': 0.0, 'fuel': 0.0, 'heat': 0.0}
    flow_emissions = {'electricity': 0.0, 'fuel': 0.0, 'heat': 0.0}
    flow_gradients = {'electricity': PositiveNegative(positive=inf, negative=inf), 'fuel': PositiveNegative(positive=inf, negative=inf), 'heat': PositiveNegative(positive=inf, negative=inf)}
    flow_rates = {'electricity': MinMax(min=0.0, max=inf), 'fuel': MinMax(min=0.0, max=inf), 'heat': MinMax(min=0.0, max=inf)}
    gradient_costs = {'electricity': PositiveNegative(positive=0.0, negative=0.0), 'fuel': PositiveNegative(positive=0.0, negative=0.0), 'heat': PositiveNegative(positive=0.0, negative=0.0)}
    initial_status = 1
    inputs = ['fuel']
    interfaces = ['electricity', 'fuel', 'heat']
    milp = {'electricity': False, 'fuel': False, 'heat': False}
    min_condenser_load = None
    number_of_status_changes = OnOff(on=inf, off=inf)
    outputs = ['electricity', 'heat']
    power_loss_index = None
    power_wo_dist_heat = MinMax(min=None, max=None)
    status_changing_costs = OnOff(on=0.0, off=0.0)
    status_inertia = OnOff(on=0, off=0)
    timeseries = None
    uid = my_chp
    """

    def __init__(self, name, inputs, outputs, *args, **kwargs):
        # The Transformer class requires the positional argument 'conversions'
        # the CHP class however doesn't, therefore if a CHP object is created
        # without the 'conversions' argument, a default value gets passed to
        # super().__init__().
        if 'conversions' not in (args or kwargs):
            kwargs.update({'conversions': es_defaults['chp_efficiency']})
        super().__init__(name, inputs, outputs, *args, **kwargs)
        # Add the additional parameters for the chp class, then call
        # _parse_arguments again.
        self._parameters_and_defaults['singular_values'].update({
            'back_pressure': es_defaults['chp_back_pressure'],
            'min_condenser_load': es_defaults['min_condenser_load'],
            'power_loss_index': es_defaults['power_loss_index'],
        })
        self._parameters_and_defaults['singular_value_mappings'].update({
            'conversion_factor_full_condensation': es_defaults[
                'chp_efficiency'],
            'conversions': es_defaults['chp_efficiency'],
        })
        self._parameters_and_defaults['namedtuples']['MinMax'].update({
            'el_efficiency_wo_dist_heat': es_defaults[
                'el_efficiency_wo_dist_heat'],
            'enthalpy_loss': es_defaults['enthalpy_loss'],
            'power_wo_dist_heat': es_defaults['power_wo_dist_heat'],
        })
        self._parse_arguments(**kwargs)

    @property
    def back_pressure(self):
        """Boolean to specify if back-pressure characteristics shall be used.
        Set to True and Q_CW_min to zero for back-pressure turbines.
        """
        return self._back_pressure

    @property
    def conversion_factor_full_condensation(self):
        r""" :class:`~collections.abc.Mapping` where the
        (inflow-name, outflow-name) tuple of the main flow is the only key and
        it's conversion efficiency when there is no tapped flow is it's value.
        Conversion efficiencies are expected to be between 0 and 1
        (:math:`\left[0, 1\right]`).
        """
        return self._conversion_factor_full_condensation

    @property
    def el_efficiency_wo_dist_heat(self):
        """Electric efficiency at min/max fuel flow without district heating.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the efficiency at that timestep.
        """
        return self._el_efficiency_wo_dist_heat

    @property
    def enthalpy_loss(self):
        """Share of flue gas loss at min/max heat extraction.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the share of flue gas enthalpy loss for that timestep.
        """
        return self._enthalpy_loss

    @property
    def min_condenser_load(self):
        """Minimal thermal condenser load to cooling water.

        Expects a list where the length is the same as the
        number of timesteps and each entry is the minimal condenser load at
        that timestep.
        """
        return self._min_condenser_load

    @property
    def power_loss_index(self):
        """Marginal loss of electric power for each additional unit of heat.

        Expects a list where the length is the same as the
        number of timesteps and each entry is a float value between 0 and 1
        giving the marginal loss of power at that timestep.
        """
        return self._power_loss_index

    @property
    def power_wo_dist_heat(self):
        """Min/max electric power without district heating.

        Expects a :class:`~tessif.frused.namedtuples.MinMax` where both the min
        and the max value are a list where the length is the same as the
        number of timesteps and each entry is the power at that timestep.
        """
        return self._power_wo_dist_heat


class Storage(AbstractEsComponent):
    r"""
    Entities only concerned with input, output and accumulation.

    Parameters
    ----------
    name: ~collections.abc.Hashable
        Identifier. Usually a string, aka a name.

    input: ~collections.abc.Hashable
        Hashable unique identifier. Usually a string specifying the
        storage-entity's input e.g::

            'electricity'

    output: ~collections.abc.Hashable
        Hashable unique identifier. Usually a string specifying the
        storage-entity's output e.g::

            'electricity'

    capacity: ~numbers.Number
        Maximum number of units the entity is able to accumulate.

    Note
    ----
    All following arguments are considered optional parameters and are
    provided using \*\*kwargs.

    Parameters
    ----------
    latitude: ~numbers.Number
        Geospatial latitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.latitude<tessif.frused.namedtuples.Uid.latitude>`
    longitude: ~numbers.Number
        Geospatial longitude in degree. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.longitude<tessif.frused.namedtuples.Uid.longitude>`
    region: str
        Arbitrary regional categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.region<tessif.frused.namedtuples.Uid.region>`
    sector: str
        Arbitrary sector categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.sector<tessif.frused.namedtuples.Uid.sector>`
    carrier: str
        Arbitrary energy carrier categorization string.Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.carrier<tessif.frused.namedtuples.Uid.carrier>`
    component: str
        One of the :ref:`energy system component identifiers
        <Models_Tessif_Concept_ESC>`.
    node_type: str
        Arbitrary node type categorization string. Parsed into a
        :class:`namedtuples.Uid<tessif.frused.namedtuples.Uid>` instance
        as :paramref:`uid.node_type<tessif.frused.namedtuples.Uid.node_type>`

    Warning
    -------
    The 6 beforneamed arguments together with :paramref:`~Storage.name`
    form an id as a :attr:`tessif.frused.namedtuples.Uid` object. This
    :attr:`~tessif.frused.namedtuples.Uid` object as well as its string
    representation (str(:attr:`~tessif.frused.namedtuples.Uid`)) must
    be unique.

    The string representation can be tweaked using
    :attr:`~tessif.frused.configurations.node_uid_style`. But in total
    the overall combination of these parameters must be unique and will form
    the components hashable uid (unique identifier)

    Parameters
    ----------
    initial_soc: ~numbers.Number, default = 0
        Amount of stored units at the beginning of the evaluated
        timeframe.

        Usually something between 0 and :paramref:`~Storage.capacity`
        (:math:`\left[0, \text{capacity}\right]`).

    final_soc: ~numbers.Number,None, default = None
        Amount of stored units at the end of the evaluated
        timeframe.

        Usually something between 0 and :paramref:`~Storage.capacity`
        (:math:`\left[0, \text{capacity}\right]`).

        If ``None``, the solver does not constrain the final soc.
        However since most :ref:`models <SupportedModels>` do not support
        constraining the final soc, this value is primarily used to force a
        state of charge equilibrium at the beginning and the end of the
        simulated timeframe. Meaning ``final_soc == initial_soc`` so
        the total energy balance of the simulated systems stays 0.

        Use ``None`` to ensure, different socs at first and last timestep
        are valid.

    idle_changes: :class:`~tessif.frused.namedtuples.PositiveNegative`
        A :class:`~tessif.frused.namedtuples.PositiveNegative`
        :class:`~typing.NamedTuple` describing state of charge changes of two
        following discrete timesteps.

    flow_rates: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going in/out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.

        **Default**::

            {key: MinMax(0, float('+inf')) for key in [*input, *output]}

    flow_efficiencies: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its efficiency.

        Meaning for each amount per time that is going in/out the amount
        times its respective efficiency is available for storing.

        **Default**::

            {k: InOut(1, 1) for k in [*input, *output]}

    flow_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going in/out this amount of
        cost-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*input, *output]}

    flow_emissions: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its emission.

        Meaning for each amount per time that is going in/out this amount of
        emission-unit is taken into account (by the solver).

        **Default**::

            {key: 0 for key in [*input, *output]}

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.

    flow_gradients: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.

        **Default**::

            {k: PositiveNegative(float('+inf'),float('+inf'))
             for k in [*input, *output]}

    gradient_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :paramref:`~Storage.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Storage.flow_rates` this
        amount of cost-unit is taken into account (by the solver).

        **Default**::

            {k: PositiveNegative(0, 0) for k in [*input, *output]}

    timeseries: ~collections.abc.Mapping, default=None
        Mapping an arbitrary number of :paramref:`input/output names<
        Storage.inputs>` to a :class:`~tessif.frused.namedtuples.MinMax` tuple
        describing the minimum and maximum :paramref:`flow_rates` respectively.

        For Example

        Setting the maximum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=0, max=np.array([10, 42]))}

        Setting the minimum :paramref:`flow_rate <flow_rates>`::

            import numpy as np
            timeseries = {'input_bus': MinMax(
                min=np.array([1, 2]), max=float('+inf'))}

        Fixing the :paramref:`flow_rate <flow_rates>` to a certain timeseries::

            import numpy as np
            timeseries = {input_bus': MinMax(
                min=np.array([1, 2]), max=np.array([1, 2]))}

    expandable: ~collections.abc.Mapping
        Mapping of each :paramref:`input <Storage.input>` and
        :paramref:`output <Storage.output>` name or ``capacity``
        to a boolean variable describing if the mapped
        :paramref:`Storage.flow_rates`/ the capacity value can be increased by
        the solver or not.

        **Default**::

            {key: False for key in [*input, *output, 'capacity']}

        For example::

            expandable: {'capacity': True, f'{Storage.output}': True}

    fixed_expansion_ratios: ~collections.abc.Mapping
        Mapping of each :paramref:`input <Storage.input>` and
        :paramref:`output <Storage.output>` name to a boolean variable
        describing if the mapped :paramref:`flow rate <Storage.flow_rates>`
        expansion is fixed in relation to the installed
        :paramref:`capacity <Storage.capacity>`.

        **Default**::

            {key: True for key in [*input, *output]}

        For example::

            {f'{Storage.input}': True, f'{Storage.output}': True}

    expansion_costs: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name <Storage.input>` or
        the keyword ``capacity`` to a :class:`~numbers.Number` specifying its
        expansion cost.

        Meaning for each unit the :paramref:`~Storage.capacity` or the
        maximum of the mapped :paramref:`amount per time<Storage.flow_rates>`
        is increased (by the solver) this amount of cost-unit is taken into
        account (by the solver).

        **Default**::

            {key: 0 for key in [*input, *output, 'capacity']}

    expansion_limits: ~collections.abc.Mapping
        Mapping of each :paramref:`input/output name<Storage.input>` or the
        keyword capacity to a :class:`~tessif.frused.namedtuples.MinMax` tuple
        describing the minimum and maximum expansion limit.

        Meaning the actual increase of the :paramref:`~Storage.capacity` or the
        mapped :paramref:`amount per time<Storage.flow_rates>` will be
        somwhere between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)

        **Default**::

            {k: MinMax(0, float('+inf'))
             for k in [*input, *output, 'capacity']}


    Note
    ----
    Providing non default parameters for the following set of arguments will
    cause the optimization problem to most likely turn into a
    `Mixed Integer Linear Problem
    <https://en.wikipedia.org/wiki/Integer_programming#Variants>`_

    Parameters
    ----------
    milp: ~collections.abc.Mapping
        Mapping of each :attr:`input/output name <Storage.input>` to a
        boolean variable describing if the mapped
        :attr:`Storage.flow_rates` parameter can be
        subject to mixed integer linear constraints.

        **Default**::

            {key: False for key in [*inputs, *outputs]}

        warning
        -------
        If :paramref:`~Storage.milp` evaluates to ``False`` following set of
        parameters is most likely ignored during optimization.

    initial_status: bool, default=True
        Status variable, indicating if the entity is running, operating,
        working, doing the things its supposed to do, in the beginning
        of the evaluated timeframe.

    status_inertia: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the minimum uptime and downtime.
        With up and downtime describing the minimum amount of following
        discrete timesteps the entity as to be operating or standing stil
        respectively.

        **Default**::

            OnOff(0, 0)

    status_changing_costs: ~tessif.frused.namedtuples.OnOff
        An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the cost for changing status
        from ``on`` to ``off`` and from ``off`` to ``on`` respectively

        **Default**::

            OnOff(0, 0)

    number_of_status_changes: ~tessif.frused.namedtuples.OnOff
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.

        **Default**::

            OnOff(float('+inf'), float('+inf'))

    costs_for_being_active: :class:`~number.Number`, default = 0
        Costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).

    Example
    -------
    Default parameterized :class:`Storage` object with no need to seperate
    in and outflow:

    >>> import pprint
    >>> from tessif.model.components import Storage
    >>> storage = Storage(
    ...     name='my_storage', input='electricity', output='electricity',
    ...     capacity=100)
    >>> print(storage.uid)
    my_storage

    >>> print(storage.input)
    electricity

    >>> print(storage.output)
    electricity

    >>> print(sorted(storage.interfaces))
    ['electricity']

    Following example transforms the frozensets into sorted lists, to enable
    doctesting

    Accessing all its :attr:`~Storage.attributes`:

    >>> for k, v in storage.attributes.items():
    ...     print('{} = {}'.format(
    ...         k, sorted(v) if isinstance(v, frozenset) else v))
    ... # frozensets are transformed to sorted list for doctesting consistency
    capacity = 100
    costs_for_being_active = 0.0
    expandable = {'capacity': False, 'electricity': False}
    expansion_costs = {'capacity': 0.0, 'electricity': 0.0}
    expansion_limits = {'capacity': MinMax(min=0.0, max=inf), 'electricity': MinMax(min=0.0, max=inf)}
    final_soc = None
    fixed_expansion_ratios = {'electricity': True}
    flow_costs = {'electricity': 0.0}
    flow_efficiencies = {'electricity': InOut(inflow=1.0, outflow=1.0)}
    flow_emissions = {'electricity': 0.0}
    flow_gradients = {'electricity': PositiveNegative(positive=inf, negative=inf)}
    flow_rates = {'electricity': MinMax(min=0.0, max=inf)}
    gradient_costs = {'electricity': PositiveNegative(positive=0.0, negative=0.0)}
    idle_changes = PositiveNegative(positive=0.0, negative=0.0)
    initial_soc = 0.0
    initial_status = 1
    input = electricity
    interfaces = ['electricity']
    milp = {'electricity': False}
    number_of_status_changes = OnOff(on=inf, off=inf)
    output = electricity
    status_changing_costs = OnOff(on=0.0, off=0.0)
    status_inertia = OnOff(on=0, off=0)
    timeseries = None
    uid = my_storage
    """

    def __init__(self, name, input, output, capacity, *args, **kwargs):
        self._input = input
        self._output = output
        self._interfaces = frozenset((self._input, self._output))
        self._capacity = capacity

        # modify this dict for adding additional parameters
        self._parameters_and_defaults = {
            'singular_values': {
                'initial_status': es_defaults['initial_status'],
                'costs_for_being_active': es_defaults[
                    'costs_for_being_active'],
                'initial_soc': es_defaults['initial_soc'],
                'final_soc': es_defaults['final_soc'],
            },
            'singular_value_mappings': {
                'flow_costs': {key: es_defaults['flow_costs']
                               for key in sorted(self._interfaces)},
                'flow_emissions': {key: es_defaults['emissions']
                                   for key in sorted(self._interfaces)},
                'expandable': {
                    key: es_defaults['expandable']
                    for key in sorted(self._interfaces)+['capacity']},
                'fixed_expansion_ratios': {
                    key: es_defaults['fixed_expansion_ratios']
                    for key in sorted(self._interfaces)},
                'expansion_costs': {
                    key: es_defaults['expansion_costs']
                    for key in sorted(self._interfaces)+['capacity']},
                'milp': {key: es_defaults['milp']
                         for key in sorted(self._interfaces)},
            },
            'namedtuples': {
                'MinMax': {
                },
                'OnOff': {
                    'status_inertia': nts.OnOff(
                        es_defaults['minimum_uptime'],
                        es_defaults['minimum_downtime']),
                    'status_changing_costs': nts.OnOff(
                        es_defaults['startup_costs'],
                        es_defaults['shutdown_costs']),
                    'number_of_status_changes': nts.OnOff(
                        es_defaults['maximum_startups'],
                        es_defaults['maximum_shutdowns']),
                },
                'PositiveNegative': {
                    'idle_changes': nts.PositiveNegative(
                        es_defaults['gain_rate'],
                        es_defaults['loss_rate']),
                },
            },
            'mapped_namedtuples': {
                'MinMax': {
                    'expansion_limits': {
                        key: nts.MinMax(
                            es_defaults['minimum_expansion'],
                            es_defaults['maximum_expansion'])
                        for key in sorted(self._interfaces)+['capacity']},
                    'flow_rates': {key: nts.MinMax(
                        es_defaults['minimum_flow_rate'],
                        es_defaults['maximum_flow_rate'])
                        for key in sorted(self._interfaces)},
                },
                'PositiveNegative': {
                    'flow_gradients': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient'],
                        es_defaults['negative_gradient'])
                        for key in sorted(self._interfaces)},
                    'gradient_costs': {key: nts.PositiveNegative(
                        es_defaults['positive_gradient_costs'],
                        es_defaults['negative_gradient_costs'])
                        for key in sorted(self._interfaces)},
                },
                'InOut': {
                    'flow_efficiencies': {key: nts.InOut(
                        es_defaults['efficiency'],
                        es_defaults['efficiency'])
                        for key in sorted(self._interfaces)},
                },
            },
            'timeseries': None,
        }

        super().__init__(name, *args, **kwargs)

    @property
    def input(self):
        """
        :class:`Hashable<collections.abc.Hashable>` unique identifier. Usually
        a string aka name representing the storage-entity's input.
        """
        return self._input

    @property
    def output(self):
        """
        :class:`Hashable<collections.abc.Hashable>` unique identifier. Usually
        a string aka name representing the storage-entity's output.
        """
        return self._output

    @property
    def capacity(self):
        r""" Maximum :class:`~numbers.Number` of units the entity is able
        to accumulate.
        """
        return self._capacity

    @property
    def initial_soc(self):
        r""" The :class:`~numbers.Number` of units the entity
        has accumulated at the beginning of the evaluated timeframe.
        Usually something between  0 and :attr:`~Storage.capacity`
        (:math:`\left[0, \text{capacity}\right]`).
        """
        return self._initial_soc

    @property
    def final_soc(self):
        r""" The :class:`~numbers.Number` of units the entity
        has accumulated at the end of the evaluated timeframe.
        Usually something between  0 and :attr:`~Storage.capacity`
        (:math:`\left[0, \text{capacity}\right]`).

        Can also be  ``None`` to not constrain the final soc.
        """
        return self._final_soc

    @property
    def idle_changes(self):
        """A :class:`~tessif.frused.namedtuples.PositiveNegative`
        :class:`~typing.NamedTuple` describing state of charge changes of two
        following discrete timesteps.
        """
        return self._idle_changes

    @property
    def flow_rates(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum amount per time.

        Meaning each flow going out during one discrete timestep is greater
        equal than the minimum amount per time and less equal than the maximum
        amount per time  mapped to its name.
        """
        return self._flow_rates

    @property
    def flow_efficiencies(self):
        """ :class:`~collections.abc.Mapping`
        of each :paramref:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its efficiency.

        Meaning for each amount per time that is going in/out the amount
        times its respective efficiency is available for storing.
        """
        return self._flow_efficiencies

    @property
    def flow_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its cost.

        Meaning for each amount per time that is going out this amount of
        cost-unit is taken into account (by the solver).
        """
        return self._flow_costs

    @property
    def flow_emissions(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Storage.input>` to a
        :class:`~numbers.Number` specifying its emissions

        Meaning for each amount per time that is going out this amount of
        emission-unit is taken into account (by the solver).

        Note
        ----
        This unit primarily serves as system wide constrain parameter as in
        'All emissions must remain below 100 units'.
        """
        return self._flow_emissions

    @property
    def flow_gradients(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the maximum positive or negative change between two following
        timesteps.

        Meaning each flow amount increase/decrease between two
        following discrete timesteps is less equal than the maximum change
        mapped to its name.
        """
        return self._flow_gradients

    @property
    def gradient_costs(self):
        """ :class:`~collections.abc.Mapping`
        Mapping of each :paramref:`input/output name<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.PositiveNegative` tuple describing
        the costs for the respective
        :attr:`~Storage.flow_gradients`.

        Meaning for each unit
        of change of its mapped :paramref:`~Storage.flow_rates` this
        amount of cost-unit is taken into account (by the solver).
        """
        return self._gradient_costs

    @property
    def timeseries(self):
        """ :class:`~collections.abc.Mapping` of an arbitrary number
        of :attr:`input/output names<Storage.input>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum :paramref:`flow_rates` respectively.
        """
        return self._timeseries

    @property
    def expandable(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name <Storage.input>` to a boolean
        variable describing if the mapped :attr:`Storage.flow_rates`
        value can be increased by the  solver or not.
        """
        return self._expandable

    @property
    def fixed_expansion_ratios(self):
        """ :class:`~collections.abc.Mapping`
        of each :paramref:`input <Storage.input>` and
        :paramref:`output <Storage.output>` name to a boolean variable
        describing if the mapped :attr:`flow rate <Storage.flow_rates>`
        expansion is fixed in relation to the installed
        :attr:`capacity <Storage.capacity>`.
        """
        return self._fixed_expansion_ratios

    @property
    def expansion_costs(self):
        """ :class:`~collections.abc.Mapping`
        of each :attr:`input/output name <Storage.input>` to a
        :class:`~numbers.Number` specifying its expansion cost.

        Meaning for each unit the maximum of the mapped
        :attr:`amount per time<Storage.flow_rates>` is increased
        (by the solver) this amount of cost-unit is taken into account
        (by the solver).
        """
        return self._expansion_costs

    @property
    def expansion_limits(self):
        r""" :class:`~collections.abc.Mapping`
        of each :attr:`input/output name <Storage.input>` to a
        :class:`~tessif.frused.namedtuples.MinMax` tuple describing the
        minimum and maximum expansion limit.

        Meaning the actual increase of the mapped
        :attr:`amount per time<Storage.flow_rates>` will be somewhere
        between the given minimum and maximum.
        (:math:`\left[\text{min}, \text{max}\right]`)
        """
        return self._expansion_limits

    @property
    def initial_status(self):
        """ :class:`Status variable <bool>`, indicating if the entity is
        running, operating, working, doing the things its supposed to do in
        the beginning of the evaluated timeframe.
        """
        return self._initial_status

    @property
    def status_inertia(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the minimum uptime and downtime. With up and downtime
        describing the minimum amount of following discrete timesteps the
        entity as to be operating or standing still respectively.
        """
        return self._status_inertia

    @property
    def status_changing_costs(self):
        """
        :class:`~tessif.frused.namedtuples.OnOff` :class:`~typing.NamedTuple`
        describing the cost for changing status from ``on`` to ``off`` and
        from ``off`` to ``on`` respectively.
        """
        return self._status_changing_costs

    @property
    def number_of_status_changes(self):
        """An :class:`~tessif.frused.namedtuples.OnOff`
        :class:`~typing.NamedTuple` describing the number of times the entity
        can change its status from ``on`` to ``off`` and from ``off`` to ``on``
        respectively.
        """
        return self._number_of_status_changes

    @property
    def costs_for_being_active(self):
        """ A :class:`~number.Number`, default = 0
        Describing the costs for not being inactive.

        Meaning for each discrete time step the entity's boolean status
        variable is ``True``, this amount of cost units is taken in to account
        (by the solver).
        """
        return self._costs_for_being_active
