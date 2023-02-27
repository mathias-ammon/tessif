.. currentmodule:: tessif.frused.spellings

Spellings
=========

.. warning:: This documentaion page is **comprehensive**.

	     Recommended way of using this doc page is the search function (strg+f)

	     Checking if a certain spelling is supported i.e. ``variable_cost`` for
	     reading in flow cost data is done by prgogramatically browsing this page:

	         1. Press ``strg+f``
		 2. Type ``variable_cost``
		 3. If nothing is found renaming the key is recommended
		 4. If somehting is found, check the table heading
		    (``flow_costs`` in this example)
		 5. Use this key as parameter for :paramref:`get_from.smth_like`
		    to map ``variable_cost`` to ``flow_costs``
		    for reading in and succesfully parsing data.


.. rubric:: Auxiliaries
.. autosummary::
   :nosignatures:

   get_from
   seperators
   variation_base


.. _Spellings_Models:
.. rubric:: Supported Models
.. autosummary::
   :nosignatures:

   calliope
   fine
   oemof
   pypsa

.. _Spellings_UidComponents:
.. rubric:: Unique Identifier Components (Parts making up the UID)
.. autosummary::
   :nosignatures:

   name
   latitude
   longitude
   region
   sector
   carrier
   node_type

.. rubric:: Time Serieses
.. autosummary::
   :nosignatures:

   timeindex
   timeseries
   timeframe

.. rubric:: Global Constraints
.. autosummary::
   :nosignatures:

   global_constraints

.. rubric:: TESSiF's Energy System Model
.. autosummary::
   :nosignatures:

   accumulated_amounts


   costs_for_being_active

   expandable
   expansion_costs
   expansion_limits

   flow_costs
   flow_emissions
   flow_gradients
   flow_rates

   gradient_costs

   idle_changes
   initial_soc
   initial_status
   inputs

   number_of_status_changes

   status_inertia
   status_changing_costs

   outputs


.. rubric:: Component Parameters as Singular Values
.. autosummary::
   :nosignatures:

   accumulated_maximum
   accumulated_minimum
   active

   efficiency
   emissions
   exogenously_set
   exogenously_set_value
   expansion_costs
   expansion_problem

   gain_rate

   input
   installed_capacity

   loss_rate

   maximum
   maximum_efficiency
   maximum_expansion

   minimum
   minimum_efficiency
   minimum_expansion
   minimum_downtime
   minimum_uptime

   negative_gradient
   negative_gradient_costs

   output

   positive_gradient
   positive_gradient_costs

   shutdown_costs
   startup_costs
   storage_capacity


.. rubric:: Input Output Seperation
.. autosummary::
   :nosignatures:

   inflow_costs
   inflow_efficiency
   inflow_emissions
   input_maximum
   input_minimum
   input_negative_gradient
   input_positive_gradient

   outflow_costs
   outflow_efficiency
   outflow_emissions
   output_maximum
   output_minimum
   output_negative_gradient
   output_positive_gradient


.. rubric:: Component Parameters as Series Values
.. autosummary::
   :nosignatures:

   efficiency_n
   emissions_n

   flow_costs_n
   fraction_n

   inflow_costs_n
   inflow_emissions_n
   input_n

   outflow_costs_n
   outflow_emissions_n
   output_n


.. rubric:: Oemof Specific Component Parameters
.. autosummary::
   :nosignatures:

   already_installed

   back_pressure

   maximum_extraction
   maximum_fuelgas_losses
   maximum_heat
   maximum_power

   milp
   minimum_extraction
   minimum_fuelgas_losses
   minimum_heat
   minimum_power

   fraction
   fuel_in
   fuelgas_losses

   heat_costs
   heat_efficiency
   heat_emissions
   heat_out

   ideal

   lower_heating_value

   nominal_value
   number_of_connections

   power_costs
   power_efficiency
   power_emissions
   power_loss_index
   power_out

   upper_heating_value

.. _Spellings_EnergySystemComponentIdentifiers:
.. rubric:: Energy System Component Identifers
.. autosummary::
   :nosignatures:

   bus
   sink
   storage
   source
   transformer
   connector

.. _Spellings_EnergySystemComponentIdentifiers_EnergyCarrier:
.. rubric:: Energy System Component Identifers - Energy Carrier
.. autosummary::
   :nosignatures:

   solar
   wind
   water
   biomass
   commodity
   gas
   oil
   lignite
   hardcoal
   nuclear
   electricity
   steam
   hot_water

.. _Spellings_EnergySystemComponentIdentifiers_Sector:
.. rubric:: Energy System Component Identifers - Sector
.. autosummary::
   :nosignatures:

   power
   heat
   mobility
   coupled


.. _Spellings_EnergySystemComponentIdentifiers_Label:
.. rubric:: Energy System Component Identifers - Label
.. autosummary::
   :nosignatures:

   renewables
   photovoltaic
   solarthermal
   onshore
   offshore
   hydro_electric
   imported
   mimo_transformer
   sito_flex_transformer
   generic_chp
   siso_nonlinear_transformer
   combined_heat_power
   power_plant
   heat_plant
   electrical_line
   gas_pipeline
   gas_delivery
   oil_pipeline
   oil_delivery
   generic_storage
   hydro_electrical_storage
   electro_chemical_storage
   electro_mechanical_storage
   thermal_energy_storage
   power2x
   backup
   export
   excess

.. rubric:: Auxilliaries
.. AUXILIARIES
.. -----------
.. automodule:: tessif.frused.spellings
   :members: get_from, to_csv

.. autodata:: tessif.frused.spellings.seperators
   :annotation:

.. autodata:: tessif.frused.spellings.variation_base
   :annotation:


.. rubric:: Supported Models
.. Supported Models
.. ----------------
.. autodata:: tessif.frused.spellings.calliope
   :annotation:
.. autodata:: tessif.frused.spellings.fine
   :annotation:
.. autodata:: tessif.frused.spellings.oemof
   :annotation:
.. autodata:: tessif.frused.spellings.pypsa
   :annotation:

.. rubric:: Unique Identifiers Components (Parts making up the UID)
.. Unique Identifiers Components (Parts making up the UID)
.. -----------
.. autodata:: tessif.frused.spellings.name
   :annotation:

.. autodata:: tessif.frused.spellings.latitude
   :annotation:

.. autodata:: tessif.frused.spellings.longitude
   :annotation:

.. autodata:: tessif.frused.spellings.region
   :annotation:

.. autodata:: tessif.frused.spellings.sector
   :annotation:

.. autodata:: tessif.frused.spellings.carrier
   :annotation:

.. autodata:: tessif.frused.spellings.node_type
   :annotation:


.. rubric:: Time Serieses
.. Time Serieses
.. -----------
.. autodata:: tessif.frused.spellings.timeframe
   :annotation:

.. autodata:: tessif.frused.spellings.timeindex
   :annotation:

.. autodata:: tessif.frused.spellings.timeseries
   :annotation:

.. rubric:: Global Constraints
.. autodata:: tessif.frused.spellings.global_constraints
   :annotation:


.. rubric:: TESSiF's Energy System Model
.. autosummary::
   :nosignatures:

.. A
.. autodata:: tessif.frused.spellings.accumulated_amounts
   :annotation:

.. C
.. autodata:: tessif.frused.spellings.costs_for_being_active
   :annotation:

.. E
.. autodata:: tessif.frused.spellings.expandable
   :annotation:

.. autodata:: tessif.frused.spellings.expansion_costs
   :annotation:

.. autodata:: tessif.frused.spellings.expansion_limits
   :annotation:

.. F
.. autodata:: tessif.frused.spellings.flow_costs
   :annotation:

.. autodata:: tessif.frused.spellings.flow_emissions
   :annotation:

.. autodata:: tessif.frused.spellings.flow_gradients
   :annotation:

.. autodata:: tessif.frused.spellings.flow_rates
   :annotation:

.. G
.. autodata:: tessif.frused.spellings.gradient_costs
   :annotation:

.. I
.. autodata:: tessif.frused.spellings.idle_changes
   :annotation:

.. autodata:: tessif.frused.spellings.initial_soc
   :annotation:

.. autodata:: tessif.frused.spellings.initial_status
   :annotation:

.. autodata:: tessif.frused.spellings.inputs
   :annotation:

.. N
.. autodata:: tessif.frused.spellings.number_of_status_changes
   :annotation:

.. S
.. autodata:: tessif.frused.spellings.status_inertia
   :annotation:

.. autodata:: tessif.frused.spellings.status_changing_costs
   :annotation:

.. O
.. autodata:: tessif.frused.spellings.outputs
   :annotation:


.. rubric:: Component Parameters as Singular Values
.. Component Parameters as Singular Values
.. ---------------------------------------
.. A
.. autodata:: tessif.frused.spellings.active
   :annotation:

.. autodata:: tessif.frused.spellings.accumulated_maximum
   :annotation:

.. autodata:: tessif.frused.spellings.accumulated_minimum
   :annotation:

.. E
.. autodata:: tessif.frused.spellings.efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.emissions
   :annotation:

.. autodata:: tessif.frused.spellings.exogenously_set
   :annotation:

.. autodata:: tessif.frused.spellings.exogenously_set_value
   :annotation:

.. autodata:: tessif.frused.spellings.expansion_problem
   :annotation:


.. G
.. autodata:: tessif.frused.spellings.gain_rate
   :annotation:


.. I

.. autodata:: tessif.frused.spellings.input
   :annotation:

.. autodata:: tessif.frused.spellings.installed_capacity
   :annotation:


.. L
.. autodata:: tessif.frused.spellings.loss_rate
   :annotation:


.. M
.. autodata:: tessif.frused.spellings.maximum
   :annotation:

.. autodata:: tessif.frused.spellings.maximum_expansion
   :annotation:

.. autodata:: tessif.frused.spellings.maximum_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.minimum
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_expansion
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_downtime
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_uptime
   :annotation:


.. N
.. autodata:: tessif.frused.spellings.negative_gradient
   :annotation:

.. autodata:: tessif.frused.spellings.negative_gradient_costs
   :annotation:


.. O
.. autodata:: tessif.frused.spellings.output
   :annotation:


.. P
.. autodata:: tessif.frused.spellings.positive_gradient
   :annotation:

.. autodata:: tessif.frused.spellings.positive_gradient_costs
   :annotation:

.. S

.. autodata:: tessif.frused.spellings.shutdown_costs
   :annotation:

.. autodata:: tessif.frused.spellings.startup_costs
   :annotation:

.. autodata:: tessif.frused.spellings.storage_capacity
   :annotation:


.. rubric:: Singular Value Input Output Seperation
.. Singular Value Input Output Seperation
.. ---------------------------------------

.. autodata:: tessif.frused.spellings.inflow_costs
   :annotation:

.. autodata:: tessif.frused.spellings.inflow_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.inflow_emissions
   :annotation:

.. autodata:: tessif.frused.spellings.input_maximum
   :annotation:

.. autodata:: tessif.frused.spellings.input_minimum
   :annotation:

.. autodata:: tessif.frused.spellings.input_negative_gradient
   :annotation:

.. autodata:: tessif.frused.spellings.input_positive_gradient
   :annotation:


.. autodata:: tessif.frused.spellings.outflow_costs
   :annotation:

.. autodata:: tessif.frused.spellings.outflow_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.outflow_emissions
   :annotation:

.. autodata:: tessif.frused.spellings.output_maximum
   :annotation:

.. autodata:: tessif.frused.spellings.output_minimum
   :annotation:

.. autodata:: tessif.frused.spellings.output_negative_gradient
   :annotation:

.. autodata:: tessif.frused.spellings.output_positive_gradient
   :annotation:


.. rubric:: Component Parameters as Series Values
.. Component Parameters as Series Values
.. -------------------------------------
.. E
.. autodata:: tessif.frused.spellings.efficiency_n
   :annotation:

.. autodata:: tessif.frused.spellings.emissions_n
   :annotation:


.. F
.. autodata:: tessif.frused.spellings.flow_costs_n
   :annotation:

.. autodata:: tessif.frused.spellings.fraction_n
   :annotation:


.. I
.. autodata:: tessif.frused.spellings.inflow_costs_n
   :annotation:

.. autodata:: tessif.frused.spellings.inflow_emissions_n
   :annotation:

.. autodata:: tessif.frused.spellings.input_n
   :annotation:


.. O
.. autodata:: tessif.frused.spellings.outflow_costs_n
   :annotation:

.. autodata:: tessif.frused.spellings.outflow_emissions_n
   :annotation:

.. autodata:: tessif.frused.spellings.output_n
   :annotation:


.. rubric:: Oemof Specific Component Parameters
.. Oemof Specific Component Parameters
.. -----------------------------------
.. A
.. autodata:: tessif.frused.spellings.already_installed
   :annotation:


.. B
.. autodata:: tessif.frused.spellings.back_pressure
   :annotation:


.. F
.. autodata:: tessif.frused.spellings.fraction
   :annotation:

.. autodata:: tessif.frused.spellings.fuel_in
   :annotation:

.. autodata:: tessif.frused.spellings.fuelgas_losses
   :annotation:


.. H
.. autodata:: tessif.frused.spellings.heat_costs
   :annotation:

.. autodata:: tessif.frused.spellings.heat_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.heat_emissions
   :annotation:

.. autodata:: tessif.frused.spellings.heat_in
   :annotation:

.. autodata:: tessif.frused.spellings.heat_out
   :annotation:


.. I
.. autodata:: tessif.frused.spellings.ideal
   :annotation:


.. L
.. autodata:: tessif.frused.spellings.lower_heating_value
   :annotation:


.. M
.. autodata:: tessif.frused.spellings.maximum_extraction
   :annotation:

.. autodata:: tessif.frused.spellings.maximum_fuelgas_losses
   :annotation:

.. autodata:: tessif.frused.spellings.maximum_heat
   :annotation:

.. autodata:: tessif.frused.spellings.maximum_power
   :annotation:

.. autodata:: tessif.frused.spellings.milp
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_extraction
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_fuelgas_losses
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_heat
   :annotation:

.. autodata:: tessif.frused.spellings.minimum_power
   :annotation:




.. N
.. autodata:: tessif.frused.spellings.nominal_value
   :annotation:

.. autodata:: tessif.frused.spellings.number_of_connections
   :annotation:


.. P
.. autodata:: tessif.frused.spellings.power_costs
   :annotation:

.. autodata:: tessif.frused.spellings.power_efficiency
   :annotation:

.. autodata:: tessif.frused.spellings.power_emissions
   :annotation:

.. autodata:: tessif.frused.spellings.power_loss_index
   :annotation:

.. autodata:: tessif.frused.spellings.power_out
   :annotation:


.. U
.. autodata:: tessif.frused.spellings.upper_heating_value
   :annotation:


.. Energy System Component Identifiers
.. rubric:: Energy System Component Identifiers
.. autodata:: tessif.frused.spellings.energy_system_component_identifiers
   :annotation:



.. rubric:: Energy System Component Identifers
.. Energy System Component Identifers
   ----------------------------------

.. autodata:: tessif.frused.spellings.bus
   :annotation:

.. autodata:: tessif.frused.spellings.sink
   :annotation:

.. autodata:: tessif.frused.spellings.storage
   :annotation:

.. autodata:: tessif.frused.spellings.source
   :annotation:

.. autodata:: tessif.frused.spellings.transformer
   :annotation:

.. autodata:: tessif.frused.spellings.connector
   :annotation:

.. Energy System Component Identifers - Energy Carrier
.. rubric:: Energy System Component Identifers - Energy Carrier

.. autodata:: tessif.frused.spellings.solar
   :annotation:

.. autodata:: tessif.frused.spellings.wind
   :annotation:

.. autodata:: tessif.frused.spellings.water
   :annotation:

.. autodata:: tessif.frused.spellings.biomass
   :annotation:

.. autodata:: tessif.frused.spellings.commodity
   :annotation:

.. autodata:: tessif.frused.spellings.gas
   :annotation:

.. autodata:: tessif.frused.spellings.oil
   :annotation:

.. autodata:: tessif.frused.spellings.lignite
   :annotation:

.. autodata:: tessif.frused.spellings.hardcoal
   :annotation:

.. autodata:: tessif.frused.spellings.nuclear
   :annotation:

.. autodata:: tessif.frused.spellings.electricity
   :annotation:

.. autodata:: tessif.frused.spellings.hot_water
   :annotation:

.. autodata:: tessif.frused.spellings.steam
   :annotation:


.. Energy System Component Identifers - Sector
.. rubric:: Energy System Component Identifers - Sector

.. autodata:: tessif.frused.spellings.power
   :annotation:

.. autodata:: tessif.frused.spellings.heat
   :annotation:

.. autodata:: tessif.frused.spellings.mobility
   :annotation:

.. autodata:: tessif.frused.spellings.coupled
   :annotation:



.. Energy System Component Identifers - Label
.. rubric:: Energy System Component Identifers - Label

.. autodata:: tessif.frused.spellings.renewables
   :annotation:

.. autodata:: tessif.frused.spellings.photovoltaic
   :annotation:

.. autodata:: tessif.frused.spellings.solarthermal
   :annotation:

.. autodata:: tessif.frused.spellings.onshore
   :annotation:

.. autodata:: tessif.frused.spellings.offshore
   :annotation:

.. autodata:: tessif.frused.spellings.hydro_electric
   :annotation:

.. autodata:: tessif.frused.spellings.mimo_transformer
   :annotation:

.. autodata:: tessif.frused.spellings.sito_flex_transformer
   :annotation:

.. autodata:: tessif.frused.spellings.generic_chp
   :annotation:

.. autodata:: tessif.frused.spellings.siso_nonlinear_transformer
   :annotation:

.. autodata:: tessif.frused.spellings.combined_heat_power
   :annotation:

.. autodata:: tessif.frused.spellings.power_plant
   :annotation:

.. autodata:: tessif.frused.spellings.heat_plant
   :annotation:

.. autodata:: tessif.frused.spellings.electrical_line
   :annotation:

.. autodata:: tessif.frused.spellings.gas_pipeline
   :annotation:

.. autodata:: tessif.frused.spellings.gas_delivery
   :annotation:

.. autodata:: tessif.frused.spellings.oil_pipeline
   :annotation:

.. autodata:: tessif.frused.spellings.oil_delivery
   :annotation:

.. autodata:: tessif.frused.spellings.generic_storage
   :annotation:

.. autodata:: tessif.frused.spellings.hydro_electrical_storage
   :annotation:

.. autodata:: tessif.frused.spellings.electro_chemical_storage
   :annotation:

.. autodata:: tessif.frused.spellings.electro_mechanical_storage
   :annotation:

.. autodata:: tessif.frused.spellings.thermal_energy_storage
   :annotation:

.. autodata:: tessif.frused.spellings.power2x
   :annotation:

.. autodata:: tessif.frused.spellings.imported
   :annotation:

.. autodata:: tessif.frused.spellings.backup
   :annotation:

.. autodata:: tessif.frused.spellings.export
   :annotation:

.. autodata:: tessif.frused.spellings.excess
   :annotation:
