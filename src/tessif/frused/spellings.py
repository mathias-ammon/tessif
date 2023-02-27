# tessif/frused/spellings.py
"""Tessif's supported spellings to facilitate input parsing.

:mod:`~tessif.frused.spellings` is a :mod:`tessif` subpackage aggregating
aliases and variations tessif is able to parse as expected during data input.

It serves as :mod:`tessif's <tessif>` main data input abstraction mechanism.
Expanding these capabilities is best done here.
"""
import collections
import logging

import strutils

import tessif.frused.namedtuples as nts
from tessif.frused.configurations import mimos

logger = logging.getLogger(__name__)


seperators = [
    "_",
    " ",
]
"""Seperators used for combined string expressions.
"""

variation_base = {
    # models
    # ------
    "oemof": (
        "oemof",
        "omf",
        "Oemof",
        "Omf",
        "OMF",
    ),
    "pypsa": (
        "pypsa",
        "PyPSA",
        "Pyppsa",
        "PyPsa",
        "PYPSA",
        "ppsa",
        "PPSA",
    ),
    "fine": ("fine", "FINE", "Fine", "fn"),
    "calliope": (
        "calliope",
        "Calliope",
        "CALLIOPE",
        "cllp",
        "Cllp",
        "caliope",
        "Caliope",
        "CALIOPE",
        "clp",
        "Clp",
    ),
    # unique identifiers
    # ------------------
    "name": ["name", "label", "designator", "id", "identifier", "uid"],
    "latitude": [
        "latitude",
        "lat",
        "parallel",
    ],
    "longitude": [
        "longitude",
        "long",
    ],
    "region": [
        "region",
        "zone",
        "locality",
        "place",
        "territory",
        "regional",
        "district",
    ],
    "sector": [
        "sector",
        "domain",
        "sectoral",
        "segment",
        "sphere",
    ],
    "carrier": [
        "carrier",
        "transporter",
        "bearer",
        "conveyor",
    ],
    "component": [
        "component",
        "identifier",
        "esci",
        "energy_system_component_identifier",
    ],
    "node_type": [
        "node_type",
        "type",
        "kind",
    ],
    # time serieses
    # -------------
    "timeframe": [
        "timeframe",
        "time_frame",
        "temporal_scope",
        "timeindex",
        "time_index",
        "timeseries",
        "time_series",
        "temporal_horizont",
    ],
    "timeindex": [
        "timeindex",
        "timeIndex",
        "time_index",
        "date_time",
        "date",
        "dates",
        "time",
        "times",
        "ti",
        "TI",
        "timeframe",
        "time_frame",
    ],
    "timeseries": [
        "time_series",
        "timeseries",
        "timeSeries",
        "times",
        "series",
    ],
    # global constraints
    # --------------------
    "global_constraints": [
        "global_constraints",
    ],
    # TESSiF's Energy System Model
    # ----------------------------
    # A
    "accumulated_amounts": [
        "accumulated_amounts",
        "amounts",
        "summed_amounts",
        "total_amounts",
    ],
    # C
    "costs_for_being_active": [
        "costs_for_being_active",
        "activity_costs",
        "stand_by_costs",
        "being_operative_costs",
    ],
    # E
    "expandable": [
        "expandable",
        "expansion_problem",
        "expansion_plan",
        "extension_plan",
        "investment",
        "development_plan",
        "expansion_corridor",
        "extension_corridor",
        "development_corridor",
        "grows",
    ],
    "expansion_costs": [
        "expansion_costs",
        "investment_costs",
        "extension_costs",
        "ec",
        "ic",
        "ep_costs",
        "et_costs",
        "exp_costs",
        "ext_costs",
        "inv_costs",
    ],
    "expansion_limits": [
        "expansion_limits",
        "expansion_boundaries",
        "extension_limits",
        "development_limits",
        "expanding_limits",
        "growth_limits",
    ],
    # F
    "fixed_expansion_ratios": [
        "fixed_expansion_ratios",
        "fixed_expansion_ratio",
        "fixed_ratio",
        "fixed_ratios",
    ],
    "flow_costs": [
        "flow_costs",
        "variable",
        "costs",
        "c",
        "vc",
        "variable_costs",
        "fc",
    ],
    "flow_efficiencies": [
        "flow_efficiencies",
    ],
    "flow_emissions": [
        "flow_emissions",
        "emissions",
        "flow_co2_emissions",
        "co2_emissions",
    ],
    "flow_gradients": [
        "flow_gradients",
        "gradients",
        "ramps",
        "flow_changes",
        "changes_per_time",
    ],
    "flow_rates": [
        "flow_rates",
        "amounts_per_time",
        "flows",
    ],
    # G
    "gradient_costs": [
        "gradient_costs",
        "ramp_costs",
        "flow_changing_costs",
        "changing_costs",
    ],
    # I
    "idle_changes": [
        "idle_changes",
        "soc_changes",
        "storage_gains_losses",
    ],
    "initial_soc": [
        "initial_soc",
        "initial_state_of_charge",
    ],
    "initial_status": [
        "initial_status",
        "init_status",
        "boundary_status",
        "initial_operating_status",
    ],
    "inputs": [
        "inputs",
        "inflows",
        "incomings",
        "enterings",
    ],
    "interfaces": [
        "interfaces",
        "interface",
        "connections",
        "inoutputs",
        "bonds",
        "ports",
        "links",
        "intersections",
    ],
    # N
    "number_of_status_changes": [
        "number_of_status_changes",
        "status_changes",
    ],
    # S
    "status_inertia": [
        "status_inertia",
        "minimum_on_off_times",
        "minimum_on_off_durations",
    ],
    "status_changing_costs": [
        "status_changing_costs",
        "on_off_switching_costs",
        "change_operating_status_costs",
    ],
    # O
    "outputs": [
        "outputs",
        "outflows",
        "outgoings",
        "exitings",
    ],
    # singular values
    # ---------------
    # A
    "accumulated_maximum": [
        "accumulated_maximum",
        "ul",
        "summed_max",
        "sm",
        "amount",
        "total_max",
        "tm",
        "upper_boundary",
        "accumulated_max",
        "ub",
    ],
    "accumulated_minimum": [
        "accumulated_minimum",
        "accumulated_min",
        "ll",
        "summed_min",
        "sm",
        "total_min",
        "tm",
        "lower_boundary",
        "lb",
    ],
    "active": [
        "active",
        "on",
        "activated",
        "working",
    ],
    # E
    "efficiency": ["efficiency", "eta", "conversion", "conversions"],
    "emissions": [
        "emissions",
        "CO2_Emissions",
        "CO2",
        "co2",
        "co2_emissions",
        "carbon_dioxide_emissions",
    ],
    "exogenously_set": [
        "exogenously_set",
        "set",
        "exogenous",
        "fixed",
        "externally_set",
    ],
    "exogenously_set_value": [
        "exogenously_set_value",
        "actual_value",
        "timeseries_value",
        "external_timeseries",
        "externally_set_value",
        "fix",
    ],
    "expansion_problem": [
        "expansion_problem",
        "expansion_plan",
        "extension_plan",
        "investment",
        "development_plan",
        "expansion_corridor",
        "extension_corridor",
        "development_corridor",
    ],
    # G
    "gain_rate": [
        "gain_rate",
        "growth",
        "gain",
        "specific_gain",
        "growth_rate",
    ],
    # I
    "input": [
        "input",
        "inputs",
        "in",
        "incoming",
        "connection_in",
        "connection",
    ],
    "installed_capacity": [
        "installed_capacity",
        "net_capacity",
        "net_installed",
    ],
    # L
    "loss_rate": [
        "loss_rate",
        "relative_losses",
        "specific_losses",
    ],
    # M
    "maximum": [
        "maximum",
        "max",
        "maximal",
        "maximum_apts",
        "max_value",
        "maximum_value",
        "maximal_value",
    ],
    "maximum_efficiency": [
        "maximum_efficiency",
        "efficiency_max",
        "eta_max",
    ],
    "maximum_expansion": [
        "maximum_expansion",
        "maximum_invest",
        "max_invest",
        "maximum_investment",
    ],
    "minimum": [
        "minimum",
        "min",
        "minimal",
        "minimum_apts",
        "min_value",
        "minimum_value",
        "minimal_value",
    ],
    "minimum_efficiency": [
        "minimum_efficiency",
        "efficiency_min",
        "eta_min",
    ],
    "minimum_expansion": [
        "minimum_expansion",
        "minimum_invest",
        "min_invest",
        "minimum_investment",
    ],
    "minimum_downtime": [
        "minimum_downtime",
        "minimum_time_off",
    ],
    "minimum_uptime": [
        "minimum_uptime",
        "minimum_time_running",
    ],
    # N
    "negative_gradient": [
        "negative_gradient",
        "gradient",
        "ng",
        "negative_ramp",
        "ramp",
        "nr",
        "power_ramp",
        "pramp",
        "heat_ramp",
        "hr",
        "maximum_negative_change",
        "maximum_negative_changes",
    ],
    "negative_gradient_costs": [
        "negative_gradient_costs",
        "gradient_cost",
        "negative_ramp_cost",
        "ramp_cost",
        "neg_ramp_cost",
        "ngc",
        "nrc",
    ],
    # O
    "output": [
        "output",
        "outputs",
        "out",
        "connection_out",
        "connection",
        "outgoing",
        "out_going",
    ],
    # P
    "positive_gradient": [
        "positive_gradient",
        "gradient",
        "pg",
        "positive_ramp",
        "ramp",
        "pr",
        "power_ramp",
        "pramp",
        "heat_ramp",
        "hr",
        "maximum_positive_change",
        "maximum_positive_changes",
    ],
    "positive_gradient_costs": [
        "positive_gradient_costs",
        "gradient_cost",
        "positive_ramp_cost",
        "ramp_cost",
        "prc",
        "pos_ramp_cost",
        "pgc",
    ],
    # S
    "shutdown_costs": [
        "shutdown_costs",
        "shutdown_cost",
        "stopping_costs",
        "stopping_cost",
        "powerdown_costs",
        "powerdown_cost",
    ],
    "startup_costs": [
        "startup_costs",
        "startup_cost",
        "starting_costs",
        "starting_cost",
        "powerup_costs",
        "powerup_cost",
    ],
    "storage_capacity": [
        "storage_capacity",
        "capacity",
        "installed_storage_capacity",
        "nominal_storage_capacity",
    ],
    # CHP
    # ---
    "conversion_factor_full_condensation": [
        "conversion_factor_full_condensation",
        "cffc",
    ],
    "el_efficiency_wo_dist_heat": [
        "el_efficiency_wo_dist_heat",
        "eta_el_wodh",
        "Eta_el_woDH",
    ],
    "enthalpy_loss": [
        "enthalpy_loss",
        "H_L_FG",
        "h_l_fg",
    ],
    "min_condenser_load": [
        "min_condenser_load",
        "Q_CW_min",
        "q_cw_min",
    ],
    "power_wo_dist_heat": ["power_wo_dist_heat", "P_woDH", "p_wodh"],
    # Input Output Separation
    # -----------------------
    # input
    "inflow_costs": [
        "inflow_costs",
        "incosts",
        "incoming_costs",
        "variable_inflow_costs",
        "specific_inflow_costs",
    ],
    "inflow_efficiency": [
        "inflow_efficiency",
    ],
    "inflow_emissions": [
        "inflow_emissions",
        "inflow_co2_emissions",
        "inflow_CO2_Emissions",
        "inflow_CO2",
        "inflow_co2",
        "inflow_carbon_dioxide_emissions",
    ],
    "input_maximum": [
        "input_maximum",
        "input_max",
        "maximum_input",
        "omax",
        "o_max",
        "maximum_performance",
        "maximum_input_apts",
        "maximum_input_apt",
    ],
    "input_minimum": [
        "input_minimum",
        "input_min",
        "minimum_input",
        "pmin",
        "p_min",
        "minimum_performance",
        "minimum_input_apts",
        "minimum_input_apt",
    ],
    "input_negative_gradient": [
        "input_negative_gradient",
        "input_gradient",
        "input_pg",
        "input_negative_ramp",
        "input_ramp",
        "input_pr",
        "input_power_ramp",
        "input_pramp",
        "input_heat_ramp",
        "input_hr",
        "maximum_input_negative_change",
        "maximum_input_negative_changes",
    ],
    "input_positive_gradient": [
        "input_positive_gradient",
        "input_gradient",
        "input_pg",
        "input_positive_ramp",
        "input_ramp",
        "input_pr",
        "input_power_ramp",
        "input_pramp",
        "input_heat_ramp",
        "input_hr" "maximum_input_positive_change",
        "maximum_input_positive_changes",
    ],
    # output
    "outflow_costs": [
        "outflow_costs",
        "outcosts",
        "outgoing_costs",
        "variable_outflow_costs",
        "specific_outflow_costs",
    ],
    "outflow_efficiency": [
        "outflow_efficiency",
    ],
    "outflow_emissions": [
        "outflow_emissions",
        "outflow_co2_emissions",
        "outflow_CO2_Emissions",
        "outflow_CO2",
        "outflow_co2",
        "outflow_carbon_dioxide_emissions",
    ],
    "output_maximum": [
        "output_max",
        "maximum_output",
        "omax",
        "o_max",
        "maximum_performance",
        "maximum_output_apts",
        "maximum_output_apt",
    ],
    "output_minimum": [
        "output_min",
        "minimum_output",
        "pmin",
        "p_min",
        "minimum_performance",
        "minimum_output_apts",
        "minimum_output_apt",
    ],
    "output_negative_gradient": [
        "output_negative_gradient",
        "output_gradient",
        "output_pg",
        "output_negative_ramp",
        "output_ramp",
        "output_pr",
        "output_power_ramp",
        "output_pramp",
        "output_heat_ramp",
        "output_hr",
        "maximum_output_negative_change",
        "maximum_output_negative_changes",
    ],
    "output_positive_gradient": [
        "output_positive_gradient",
        "output_gradient",
        "output_pg",
        "output_positive_ramp",
        "output_ramp",
        "output_pr",
        "output_power_ramp",
        "output_pramp",
        "output_heat_ramp",
        "output_hr",
        "maximum_output_positive_change",
        "maximum_output_positive_changes",
    ],
    # Singular Value Series
    # ----------------------
    # E
    "efficiency_n": ["USES EFFICIENCY"],
    "emissions_n": ["USES CO2 EMISSIONS"],
    # F
    "flow_costs_n": ["USES FLOW COSTS"],
    "fraction_n": ["USES FRACTION"],
    # I
    "inflow_costs_n": ["USES INFLOW COSTS"],
    "inflow_emissions_n": ["USES CO2 EMISSIONS"],
    "input_n": [
        "USES CONNECTION IN",
    ],
    # O
    "outflow_costs_n": ["USES OUTFLOW COSTS"],
    "outflow_emissions_n": ["USES CO2 EMISSIONS"],
    "output_n": [
        "USES CONNECTION OUT",
    ],
    # Oemof Model Specifics
    # ---------------------
    # A
    "already_installed": [
        "already_installed",
        "existing",
        "installed",
        "initially_installed",
        "pre_installed",
    ],
    # B
    "back_pressure": ["back_pressure"],
    # F
    "fraction": ["fraction", "frct", "part"],
    "fuel_in": [
        "fuel_in",
        "fuel_input",
        "fueling",
        "fossil_fuel",
    ],
    "fuelgas_losses": [
        "fuelgas_losses",
        "flg_losses",
    ],
    # H
    "heat_costs": [
        "heat_costs",
        "heat_generation_costs",
    ],
    "heat_efficiency": [
        "heat_efficiency",
        "hefficiency",
        "heff",
        "heta",
        "heat_eta",
    ],
    "heat_emissions": [
        "heat_emissions",
        "heat_co2_emissions",
        "electricity_emissions",
    ],
    "heat_in": ["heat_in"],
    "heat_out": ["heat_out"],
    # I
    "ideal": ["ideal", "Ideal", "perfect", "Perfect"],
    # L
    "lower_heating_value": [
        "lower_heating_value",
    ],
    # M
    "maximum_extraction": [
        "maximum_extraction",
        "extraction_max",
    ],
    "maximum_fuelgas_losses": [
        "maximum_fuelgas_losses",
        "fuelgas_losses_max",
        "flg_losses_max",
    ],
    "maximum_heat": [
        "maximum_heat",
        "max_heat",
        "qmax",
        "q_max",
    ],
    "maximum_power": [
        "maximum_power",
        "power_max",
        "pmax",
        "p_max",
    ],
    "milp": [
        "milp",
        "milp_problem",
        "nonconvex",
        "nonconvex_problem",
        "mixed_integer_linear",
    ],
    "minimum_extraction": [
        "minimum_extraction",
        "extraction_min",
    ],
    "minimum_fuelgas_losses": [
        "fuelgas_losses_minimum",
        "flg_losses_min",
        "fuelgas_losses_min",
    ],
    "minimum_heat": [
        "minimum_heat",
        "heat_min",
        "qmin",
        "q_min",
    ],
    "minimum_power": [
        "minimum_power",
        "power_min",
        "pmin",
        "p_min",
    ],
    # N
    "nominal_value": [
        "nominal_value",
        "net",
        "nominal",
    ],
    "number_of_connections": [
        "number_of_connections",
        "number_connections",
        "num_connections",
    ],
    # P
    "power_costs": [
        "power_costs",
        "electricity_generation_costs",
        "electricity_costs",
        "power_generation_costs",
    ],
    "power_efficiency": [
        "power_efficiency",
        "pefficiency",
        "peff",
        "peta" "power_eta",
    ],
    "power_emissions": [
        "power_emissions",
        "power_co2_emissions",
        "electricity_emissions",
    ],
    "power_loss_index": [
        "power_loss_index",
        "beta",
    ],
    "power_out": ["power_out"],
    # U
    "upper_heating_value": [
        "upper_heating_value",
    ],
    # Energy System Component Identifiers
    # -----------------------------------
    "bus": [
        "bus",
        "hub",
        "grid",
        "network",
        "net",
        "busses",
    ],
    "source": ["source", "sources"],
    "sink": [
        "sink",
        "sinks",
    ],
    "transformer": [
        "transformer",
        "transformers",
    ],
    "storage": ["storage", "storages"],
    "connector": [
        "connectors",
        "connector",
        "link",
        "line",
        "connection",
        "interlink",
        "connection",
    ],
    # Energy Carrier
    "commodity": [
        "commodity",
    ],
    "hardcoal": ["hardcoal", "coal", "hard_coal", "black_coal"],
    "lignite": [
        "lignite",
        "browncoal",
        "brown_coal",
    ],
    "gas": [
        "gas",
        "natural_gas",
        "methane",
        "CH4",
        "ch4",
        "naturalgas",
    ],
    "oil": ["oil"],
    "solar": [
        "solar",
        "sun",
        "radiation",
        "radiative",
    ],
    "wind": [
        "wind",
        "air",
    ],
    "water": [
        "water",
        "river",
        "H2O",
        "h2o",
        "liquid_water",
    ],
    "hot_water": [
        "hot_water",
        "hot_wtr",
        "hwater",
        "hwtr",
    ],
    "steam": [
        "steam",
        "vapour",
        "vapor",
        "gaseous_water",
    ],
    "biomass": [
        "biomass",
        "bio",
        "bm",
        "bio_mass",
    ],
    "electricity": [
        "electricity",
        "electrical",
        "current",
    ],
    # Sector
    "power": ["power", "electrical", "electricity"],
    "heat": [
        "heat",
        "heating",
    ],
    "mobility": [
        "mobility",
        "traffic",
    ],
    "coupled": [
        "coupled",
        "multi_sectoral",
        "mixed",
        "combined",
        "inter_sectoral",
        "trans_sectoral",
    ],
    # Name
    "renewables": [
        "renewables",
        "renewable",
    ],
    "onshore": ["onshore", "on_shore", "wind_on", "wind_onshore", "won"],
    "offshore": ["offshore", "off_shore", "wind_off", "wind_offshore"],
    "photovoltaic": [
        "photovoltaic",
        "pv",
        "solar",
        "PV",
        "solar_power",
        "solar_panel",
    ],
    "solarthermal": [
        "solarthermal",
        "solar_thermal",
        "st",
        "ST",
        "solar_heat",
    ],
    "hydro_electric": [
        "hydro_electric",
        "impoundment",
        "dam",
        "diversion",
        "run_of_river",
        "running_water",
        "river",
    ],
    "imported": [
        "imported",
        "import",
    ],
    "backup": [
        "backup",
        "fallback",
        "reserve",
    ],
    "mimo_transformer": [
        "mimo_transformer",
        "mimo_transformers",
        "transformer",
        "transformers",
    ],
    "sito_flex_transformer": [
        "sito_flex_transformer",
        "sito_flex_chp",
        "sito_flex_transformers",
        "sito_flex_chps",
    ],
    "siso_nonlinear_transformer": [
        "siso_nonlinear_transformer",
        "offset_transformer",
    ],
    "generic_chp": [
        "generic_chp",
        "generic_chps",
        "sito_chp",
        "sito_chps",
    ],
    "combined_heat_power": [
        "combined_heat_power",
        "chp",
        "CHP",
        "chps",
        "CHPS",
        "combined",
        "power_heat",
        "chp_plant",
    ],
    "power_plant": [
        "power_plant",
        "pp",
        "PP",
        "fossil",
        "conventional",
        "generator",
    ],
    "heat_plant": [
        "heat_plant",
        "hp",
        "HP",
        "boiler",
    ],
    "electrical_line": [
        "electrical_line",
        "power_line",
        "line",
        "cable",
        "wire",
        "electricity_line",
        "powerline",
        "power_grid",
    ],
    "gas_station": [
        "gas_station",
        "gas",
    ],
    "gas_pipeline": [
        "gas_pipeline",
        "gas_line",
        "gas_grid",
        "gas_network",
        "pipeline",
    ],
    "gas_delivery": [
        "gas_delivery",
        "gas_transport",
        "gas_transportation",
    ],
    "oil_delivery": [
        "oil_delivery",
        "oil_transport",
        "oil_transportation",
    ],
    "oil_pipeline": ["oil_pipeline", "oil_line", "oil_grid", "oil_network"],
    "generic_storage": ["generic_storage", "generic_storages", "storage", "storages"],
    "electro_chemical_storage": [
        "electro_chemical_storage",
        "ecs",
        "ECS",
        "battery",
        "accu",
        "accumulator",
        "power_2_power",
    ],
    "hydro_electrical_storage": [
        "hydro_electrical_storage",
        "hes",
        "HES",
        "pump_storage",
    ],
    "electro_mechanical_storage": [
        "electro_mechanical_storage",
        "ems",
        "compressed_air_energy_storage",
        "flywheel",
        "EMS",
    ],
    "thermal_energy_storage": ["thermal_energy_storage", "tes", "TES", "heat_storage"],
    "power2x": [
        "power_to_x",
        "power_2_x",
        "power_2_gas",
        "power_to_gas",
    ],
    "power2heat": [
        "power_to_heat",
        "power_2_heat",
        "p2h",
    ],
    "demand": [
        "demand",
        "demands",
        "needs",
    ],
    "export": [
        "export",
    ],
    "excess": [
        "excess",
    ],
}
"""
Variation base keys used for creating possible spellings.

Each of the following strings is a key to a "many->one" string representation
mapping.

There is an
identically named attribute for each mapping in :mod:`tessif.frused.spellings`.
"""

# Data Input Dictionary Keys
timeindex = set()
for string in variation_base["timeindex"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            timeindex.add(variation)
timeindex = sorted(timeindex)
"""Supported ``timeindex`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/timeindex.csv
"""

timeseries = set()
for string in variation_base["timeseries"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            timeseries.add(variation)
timeseries = sorted(timeseries)
"""Supported ``timeseries`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/timeseries.csv
"""

timeframe = set()
for string in variation_base["timeframe"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            timeframe.add(variation)
timeframe = sorted(timeframe)
"""Supported ``timeframe`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/timeframe.csv
"""

global_constraints = set()
for string in variation_base["global_constraints"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            global_constraints.add(variation)
global_constraints = sorted(global_constraints)
"""Supported ``global_constraints`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/global_constraints.csv
"""

# TESSiF's  Energy System Model
# -----------------------------

accumulated_amounts = set()
for string in variation_base["accumulated_amounts"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            accumulated_amounts.add(variation)
accumulated_amounts = sorted(accumulated_amounts)
"""Supported ``accumulated_amounts`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/accumulated_amounts.csv
"""

costs_for_being_active = set()
for string in variation_base["costs_for_being_active"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            costs_for_being_active.add(variation)
costs_for_being_active = sorted(costs_for_being_active)
"""Supported ``costs_for_being_active`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/costs_for_being_active.csv
"""

expandable = set()
for string in variation_base["expandable"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            expandable.add(variation)
expandable = sorted(expandable)
"""Supported ``expandable`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/expandable.csv
"""

expansion_costs = set()
for string in variation_base["expansion_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            expansion_costs.add(variation)
expansion_costs = sorted(expansion_costs)
"""Supported ``expansion_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/expansion_costs.csv
"""

expansion_limits = set()
for string in variation_base["expansion_limits"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            expansion_limits.add(variation)
expansion_limits = sorted(expansion_limits)
"""Supported ``expansion_limits`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/expansion_limits.csv
"""

fixed_expansion_ratios = set()
for string in variation_base["fixed_expansion_ratios"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            fixed_expansion_ratios.add(variation)
fixed_expansion_ratios = sorted(fixed_expansion_ratios)
"""Supported ``fixed_expansion_ratios`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/fixed_expansion_ratios.csv
"""

flow_costs = set()
for string in variation_base["flow_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            flow_costs.add(variation)
flow_costs = sorted(flow_costs)
"""Supported ``flow_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_costs.csv
"""

flow_efficiencies = set()
for string in variation_base["flow_efficiencies"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            flow_efficiencies.add(variation)
flow_efficiencies = sorted(flow_efficiencies)
"""Supported ``flow_efficiencies`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_efficiencies.csv
"""

flow_emissions = set()
for string in variation_base["flow_emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            flow_emissions.add(variation)
flow_emissions = sorted(flow_emissions)
"""Supported ``flow_emissions`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_emissions.csv
"""

flow_gradients = set()
for string in variation_base["flow_gradients"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            flow_gradients.add(variation)
flow_gradients = sorted(flow_gradients)
"""Supported ``flow_gradients`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_gradients.csv
"""

flow_rates = set()
for string in variation_base["flow_rates"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            flow_rates.add(variation)
flow_rates = sorted(flow_rates)
"""Supported ``flow_rates`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_rates.csv
"""

gradient_costs = set()
for string in variation_base["gradient_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gradient_costs.add(variation)
gradient_costs = sorted(gradient_costs)
"""Supported ``gradient_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/gradient_costs.csv
"""

idle_changes = set()
for string in variation_base["idle_changes"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            idle_changes.add(variation)
idle_changes = sorted(idle_changes)
"""Supported ``idle_changes`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/idle_changes.csv
"""

initial_soc = set()
for string in variation_base["initial_soc"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            initial_soc.add(variation)
initial_soc = sorted(initial_soc)
"""Supported ``initial_soc`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/initial_soc.csv
"""

initial_status = set()
for string in variation_base["initial_status"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            initial_status.add(variation)
initial_status = sorted(initial_status)
"""Supported ``initial_status`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/initial_status.csv
"""

inputs = set()
for string in variation_base["inputs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            inputs.add(variation)
inputs = sorted(inputs)
"""Supported ``inputs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/inputs.csv
"""

interfaces = set()
for string in variation_base["interfaces"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            interfaces.add(variation)
interfaces = sorted(interfaces)
"""Supported ``interfaces`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/interfaces.csv
"""

number_of_status_changes = set()
for string in variation_base["number_of_status_changes"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            number_of_status_changes.add(variation)
number_of_status_changes = sorted(number_of_status_changes)
"""Supported ``number_of_status_changes`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/number_of_status_changes.csv
"""

status_inertia = set()
for string in variation_base["status_inertia"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            status_inertia.add(variation)
status_inertia = sorted(status_inertia)
"""Supported ``status_inertia`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/status_inertia.csv
"""

status_changing_costs = set()
for string in variation_base["status_changing_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            status_changing_costs.add(variation)
status_changing_costs = sorted(status_changing_costs)
"""Supported ``status_changing_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/status_changing_costs.csv
"""

outputs = set()
for string in variation_base["outputs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            outputs.add(variation)
outputs = sorted(outputs)
"""Supported ``outputs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/outputs.csv
"""

# Singular Values
# ---------------

active = set()
for string in variation_base["active"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            active.add(variation)
active = sorted(active)
"""Supported ``active`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/active.csv
"""

expansion_problem = set()
for string in variation_base["expansion_problem"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            expansion_problem.add(variation)
expansion_problem = sorted(expansion_problem)
"""Supported ``expansion_problem`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/expansion_problem.csv
"""

minimum_expansion = set()
for string in variation_base["minimum_expansion"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_expansion.add(variation)
minimum_expansion = sorted(minimum_expansion)
"""Supported ``minimum_expansion`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_expansion.csv
"""

maximum_expansion = set()
for string in variation_base["maximum_expansion"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_expansion.add(variation)
maximum_expansion = sorted(maximum_expansion)
"""Supported ``maximum_expansion`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_expansion.csv
"""

expansion_costs = set()
for string in variation_base["expansion_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            expansion_costs.add(variation)
expansion_costs = sorted(expansion_costs)
"""Supported ``expansion_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/expansion_costs.csv
"""

oemof = set()
for string in variation_base["oemof"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            oemof.add(variation)
oemof = sorted(oemof)
"""Supported ``oemof`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/oemof.csv
"""

pypsa = set()
for string in variation_base["pypsa"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            pypsa.add(variation)
pypsa = sorted(pypsa)
"""Supported ``pypsa`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/pypsa.csv
"""

fine = set()
for string in variation_base["fine"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            fine.add(variation)
fine = sorted(fine)
"""Supported ``fine`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/fine.csv
"""

calliope = set()
for string in variation_base["calliope"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            calliope.add(variation)
calliope = sorted(calliope)
"""Supported ``calliope`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/calliope.csv
"""

name = set()
for string in variation_base["name"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            name.add(variation)
name = sorted(name)
"""Supported ``name`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/name.csv
"""

latitude = set()
for string in variation_base["latitude"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            latitude.add(variation)
latitude = sorted(latitude)
"""Supported ``latitude`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/latitude.csv
"""

longitude = set()
for string in variation_base["longitude"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            longitude.add(variation)
longitude = sorted(longitude)
"""Supported ``longitude`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/longitude.csv
"""

region = set()
for string in variation_base["region"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            region.add(variation)
region = sorted(region)
"""Supported ``region`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/region.csv
"""

sector = set()
for string in variation_base["sector"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            sector.add(variation)
sector = sorted(sector)
"""Supported ``sector`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/sector.csv
"""

carrier = set()
for string in variation_base["carrier"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            carrier.add(variation)
carrier = sorted(carrier)
"""Supported ``carrier`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/carrier.csv
"""

component = set()
for string in variation_base["component"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            component.add(variation)
component = sorted(component)
"""Supported ``component`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/component.csv
"""

node_type = set()
for string in variation_base["node_type"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            node_type.add(variation)
node_type = sorted(node_type)
"""Supported ``node_type`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/node_type.csv
"""

number_of_connections = set()
for string in variation_base["number_of_connections"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            number_of_connections.add(variation)
number_of_connections = sorted(number_of_connections)
"""Supported ``number_of_connections`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/number_of_connections.csv
"""

conversion_factor_full_condensation = set()
for string in variation_base["conversion_factor_full_condensation"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            conversion_factor_full_condensation.add(variation)
conversion_factor_full_condensation = sorted(conversion_factor_full_condensation)
"""Supported ``conversion_factor_full_condensation`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/conversion_factor_full_condensation.csv
"""

el_efficiency_wo_dist_heat = set()
for string in variation_base["el_efficiency_wo_dist_heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            el_efficiency_wo_dist_heat.add(variation)
el_efficiency_wo_dist_heat = sorted(el_efficiency_wo_dist_heat)
"""Supported ``el_efficiency_wo_dist_heat`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/el_efficiency_wo_dist_heat.csv
"""

enthalpy_loss = set()
for string in variation_base["enthalpy_loss"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            enthalpy_loss.add(variation)
enthalpy_loss = sorted(enthalpy_loss)
"""Supported ``enthalpy_loss`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/enthalpy_loss.csv
"""

min_condenser_load = set()
for string in variation_base["min_condenser_load"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            min_condenser_load.add(variation)
min_condenser_load = sorted(min_condenser_load)
"""Supported ``min_condenser_load`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/min_condenser_load.csv
"""

power_wo_dist_heat = set()
for string in variation_base["power_wo_dist_heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_wo_dist_heat.add(variation)
power_wo_dist_heat = sorted(power_wo_dist_heat)
"""Supported ``power_wo_dist_heat`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_wo_dist_heat.csv
"""

fraction = set()
for string in variation_base["fraction"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            fraction.add(variation)
fraction = sorted(fraction)
"""Supported ``fraction`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/fraction.csv
"""

fraction_n = set()
for string in variation_base["fraction"]:
    for sep in seperators:
        for i in range(mimos):
            fraction_n.add(string + str(i))
            fraction_n.add(string + sep + str(i))
fraction_n = sorted(fraction_n)
"""Supported ``fraction_n`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/fractionN.csv
"""

input = set()
for string in variation_base["input"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            input.add(variation)
input = sorted(input)
"""Supported ``input`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/input.csv
"""

input_n = set()
for string in variation_base["input"]:
    for sep in seperators:
        for i in range(mimos):
            input_n.add(string + str(i))
            input_n.add(string + sep + str(i))
input_n = sorted(input_n)
"""Supported ``input_n`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/inputN.csv
"""

input_maximum = set()
for string in variation_base["input_maximum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            input_maximum.add(variation)
input_maximum = sorted(input_maximum)
"""Supported ``input_maximum`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/input_maximum.csv
"""

input_minimum = set()
for string in variation_base["input_minimum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            input_minimum.add(variation)
input_minimum = sorted(input_minimum)
"""Supported ``input_minimum`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/input_minimum.csv
"""

fuel_in = set()
for string in variation_base["fuel_in"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            fuel_in.add(variation)
fuel_in = sorted(fuel_in)
"""Supported ``fuel_in`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/fuel_in.csv
"""

output = set()
for string in variation_base["output"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            output.add(variation)
output = sorted(output)
"""Supported ``output`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/output.csv
"""

output_n = set()
for string in variation_base["output"]:
    for sep in seperators:
        for i in range(mimos):
            output_n.add(string + str(i))
            output_n.add(string + sep + str(i))
output_n = sorted(output_n)
"""Supported ``output_n`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/outputN.csv
"""

output_maximum = set()
for string in variation_base["output_maximum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            output_maximum.add(variation)
output_maximum = sorted(output_maximum)
"""Supported ``output_maximum`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/output_maximum.csv
"""

output_minimum = set()
for string in variation_base["output_minimum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            output_minimum.add(variation)
output_minimum = sorted(output_minimum)
"""Supported ``output_minimum`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/output_minimum.csv
"""

efficiency = set()
for string in variation_base["efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            efficiency.add(variation)
efficiency = sorted(efficiency)
"""Supported ``efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/efficiency.csv
"""

efficiency_n = set()
for string in variation_base["efficiency"]:
    for sep in seperators:
        for i in range(mimos):
            efficiency_n.add(string + str(i))
            efficiency_n.add(string + sep + str(i))
efficiency_n = sorted(efficiency_n)
"""Supported ``efficiency_n`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/efficiencyN.csv
"""

maximum_efficiency = set()
for string in variation_base["maximum_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_efficiency.add(variation)
maximum_efficiency = sorted(maximum_efficiency)
"""Supported ``maximum_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_efficiency.csv
"""

minimum_efficiency = set()
for string in variation_base["minimum_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_efficiency.add(variation)
minimum_efficiency = sorted(minimum_efficiency)
"""Supported ``minimum_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_efficiency.csv
"""

inflow_efficiency = set()
for string in variation_base["inflow_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            inflow_efficiency.add(variation)
inflow_efficiency = sorted(inflow_efficiency)
"""Supported ``inflow_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/inflow_efficiency.csv
"""

outflow_efficiency = set()
for string in variation_base["outflow_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            outflow_efficiency.add(variation)
outflow_efficiency = sorted(outflow_efficiency)
"""Supported ``outflow_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/outflow_efficiency.csv
"""

loss_rate = set()
for string in variation_base["loss_rate"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            loss_rate.add(variation)
loss_rate = sorted(loss_rate)
"""Supported ``loss_rate`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/loss_rate.csv
"""

power_out = set()
for string in variation_base["power_out"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_out.add(variation)
power_out = sorted(power_out)
"""Supported ``power_out`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_out.csv
"""

maximum_power = set()
for string in variation_base["maximum_power"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_power.add(variation)
maximum_power = sorted(maximum_power)
"""Supported ``maximum_power`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_power.csv
"""

minimum_power = set()
for string in variation_base["minimum_power"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_power.add(variation)
minimum_power = sorted(minimum_power)
"""Supported ``minimum_power`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_power.csv
"""

power_efficiency = set()
for string in variation_base["power_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_efficiency.add(variation)
power_efficiency = sorted(power_efficiency)
"""Supported ``power_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_efficiency.csv
"""

power_costs = set()
for string in variation_base["power_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_costs.add(variation)
power_costs = sorted(power_costs)
"""Supported ``power_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_costs.csv
"""

power_emissions = set()
for string in variation_base["power_emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_emissions.add(variation)
power_emissions = sorted(power_emissions)
"""Supported ``power_emissions`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_emissions.csv
"""

heat_out = set()
for string in variation_base["heat_out"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_out.add(variation)
heat_out = sorted(heat_out)
"""Supported ``heat_out`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/heat_out.csv
"""

heat_in = set()
for string in variation_base["heat_in"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_in.add(variation)
heat_in = sorted(heat_in)
"""Supported ``heat_in`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/heat_in.csv
"""

maximum_heat = set()
for string in variation_base["maximum_heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_heat.add(variation)
maximum_heat = sorted(maximum_heat)
"""Supported ``maximum_heat`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_heat.csv
"""

minimum_heat = set()
for string in variation_base["minimum_heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_heat.add(variation)
minimum_heat = sorted(minimum_heat)
"""Supported ``minimum_heat`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_heat.csv
"""

heat_efficiency = set()
for string in variation_base["heat_efficiency"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_efficiency.add(variation)
heat_efficiency = sorted(heat_efficiency)
"""Supported ``heat_efficiency`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/heat_efficiency.csv
"""

heat_costs = set()
for string in variation_base["heat_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_costs.add(variation)
heat_costs = sorted(heat_costs)
"""Supported ``heat_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/heat_costs.csv
"""

heat_emissions = set()
for string in variation_base["heat_emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_emissions.add(variation)
heat_emissions = sorted(heat_emissions)
"""Supported ``heat_emissions`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/heat_emissions.csv
"""

maximum_extraction = set()
for string in variation_base["maximum_extraction"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_extraction.add(variation)
maximum_extraction = sorted(maximum_extraction)
"""Supported ``maximum_extraction`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_extraction.csv
"""

minimum_extraction = set()
for string in variation_base["minimum_extraction"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_extraction.add(variation)
minimum_extraction = sorted(minimum_extraction)
"""Supported ``minimum_extraction`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_extraction.csv
"""

fuelgas_losses = set()
for string in variation_base["fuelgas_losses"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            fuelgas_losses.add(variation)
fuelgas_losses = sorted(fuelgas_losses)
"""Supported ``fuelgas_losses`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/fuelgas_losses.csv
"""

maximum_fuelgas_losses = set()
for string in variation_base["maximum_fuelgas_losses"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum_fuelgas_losses.add(variation)
maximum_fuelgas_losses = sorted(maximum_fuelgas_losses)
"""Supported ``maximum_fuelgas_losses`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/maximum_fuelgas_losses.csv
"""

minimum_fuelgas_losses = set()
for string in variation_base["minimum_fuelgas_losses"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_fuelgas_losses.add(variation)
minimum_fuelgas_losses = sorted(minimum_fuelgas_losses)
"""Supported ``minimum_fuelgas_losses`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_fuelgas_losses.csv
"""

upper_heating_value = set()
for string in variation_base["upper_heating_value"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            upper_heating_value.add(variation)
upper_heating_value = sorted(upper_heating_value)
"""Supported ``upper_heating_value`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/upper_heating_value.csv
"""

lower_heating_value = set()
for string in variation_base["lower_heating_value"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            lower_heating_value.add(variation)
lower_heating_value = sorted(lower_heating_value)
"""Supported ``lower_heating_value`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/lower_heating_value.csv
"""

power_loss_index = set()
for string in variation_base["power_loss_index"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_loss_index.add(variation)
power_loss_index = sorted(power_loss_index)
"""Supported ``power_loss_index`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/power_loss_index.csv
"""

back_pressure = set()
for string in variation_base["back_pressure"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            back_pressure.add(variation)
back_pressure = sorted(back_pressure)
"""Supported ``back_pressure`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/back_pressure.csv
"""

gain_rate = set()
for string in variation_base["gain_rate"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gain_rate.add(variation)
gain_rate = sorted(gain_rate)
"""Supported ``gain_rate`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/gain_rate.csv
"""

flow_costs_n = set()
for string in variation_base["flow_costs"]:
    for sep in seperators:
        for i in range(mimos):
            flow_costs_n.add(string + str(i))
            flow_costs_n.add(string + sep + str(i))
flow_costs_n = sorted(flow_costs_n)
"""Supported ``flow_costs_n`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/flow_costsN.csv
"""

inflow_costs = set()
for string in variation_base["inflow_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            inflow_costs.add(variation)
inflow_costs = sorted(inflow_costs)
"""Supported ``inflow_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/inflow_costs.csv
"""

inflow_costs_n = set()
for string in variation_base["inflow_costs"]:
    for sep in seperators:
        for i in range(mimos):
            inflow_costs_n.add(string + str(i))
            inflow_costs_n.add(string + sep + str(i))
inflow_costs_n = sorted(inflow_costs_n)
"""Supported ``inflow_costs_n`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/inflow_costsN.csv
"""

outflow_costs = set()
for string in variation_base["outflow_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            outflow_costs.add(variation)
outflow_costs = sorted(outflow_costs)
"""Supported ``outflow_costs`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/outflow_costs.csv
"""

outflow_costs_n = set()
for string in variation_base["outflow_costs"]:
    for sep in seperators:
        for i in range(mimos):
            outflow_costs_n.add(string + str(i))
            outflow_costs_n.add(string + sep + str(i))
outflow_costs_n = sorted(outflow_costs_n)
"""Supported ``outflow_costs_n`` spellings.

    import tessif.frused.spellings as sps
    sps.to_csv(sps.outflow_costs_n, 'outflow_costs_n', columns=6)

.. csv-table::
   :file: docs/source/csvs/spellings/outflow_costsN.csv
"""

emissions = set()
for string in variation_base["emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            emissions.add(variation)
emissions = sorted(emissions)
"""Supported ``emissions`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/emissions.csv
"""

emissions_n = set()
for string in variation_base["emissions"]:
    for sep in seperators:
        for i in range(mimos):
            emissions_n.add(string + str(i))
            emissions_n.add(string + sep + str(i))
emissions_n = sorted(emissions_n)
"""Supported ``emissions_n`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/emissionsN.csv
"""

inflow_emissions = set()
for string in variation_base["inflow_emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            inflow_emissions.add(variation)
inflow_emissions = sorted(inflow_emissions)
"""Supported ``inflow_emissions`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/inflow_emissions.csv
"""

inflow_emissions_n = set()
for string in variation_base["inflow_emissions"]:
    for sep in seperators:
        for i in range(mimos):
            inflow_emissions_n.add(string + str(i))
            inflow_emissions_n.add(string + sep + str(i))
inflow_emissions_n = sorted(inflow_emissions_n)
"""Supported ``inflow_emissions_n`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/inflow_emissionsN.csv
"""

outflow_emissions = set()
for string in variation_base["outflow_emissions"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            outflow_emissions.add(variation)
outflow_emissions = sorted(outflow_emissions)
"""Supported ``outflow_emissions`` spellings

.. csv-table::
   :file: docs/source/csvs/spellings/outflow_emissions.csv
"""

outflow_emissions_n = set()
for string in variation_base["outflow_emissions"]:
    for sep in seperators:
        for i in range(mimos):
            outflow_emissions_n.add(string + str(i))
            outflow_emissions_n.add(string + sep + str(i))
outflow_emissions_n = sorted(outflow_emissions_n)
"""Supported ``outflow_emissions_n`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/outflow_emissionsN.csv
"""

ideal = set()
for string in variation_base["ideal"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            ideal.add(variation)
ideal = sorted(ideal)
"""Supported ``ideal`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/ideal.csv
"""

storage_capacity = set()
for string in variation_base["storage_capacity"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            storage_capacity.add(variation)
storage_capacity = sorted(storage_capacity)
"""Supported ``storage_capacity`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/storage_capacity.csv
"""

installed_capacity = set()
for string in variation_base["installed_capacity"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            installed_capacity.add(variation)
installed_capacity = sorted(installed_capacity)
"""Supported ``installed_capacity`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/installed_capacity.csv
"""

nominal_value = set()
for string in variation_base["nominal_value"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            nominal_value.add(variation)
nominal_value = sorted(nominal_value)
"""Supported ``nominal_value`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/nominal_value.csv
"""

accumulated_minimum = set()
for string in variation_base["accumulated_minimum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            accumulated_minimum.add(variation)
accumulated_minimum = sorted(accumulated_minimum)
"""Supported ``accumulated_minimum`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/accumulated_minimum.csv
"""

accumulated_maximum = set()
for string in variation_base["accumulated_maximum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            accumulated_maximum.add(variation)
accumulated_maximum = sorted(accumulated_maximum)
"""Supported ``accumulated_maximum`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/accumulated_maximum.csv
"""

minimum = set()
for string in variation_base["minimum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum.add(variation)
minimum = sorted(minimum)
"""Supported ``minimum`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/minimum.csv
"""

maximum = set()
for string in variation_base["maximum"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            maximum.add(variation)
maximum = sorted(maximum)
"""Supported ``maximum`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/maximum.csv
"""

positive_gradient = set()
for string in variation_base["positive_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            positive_gradient.add(variation)
positive_gradient = sorted(positive_gradient)
"""Supported ``positive_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/positive_gradient.csv
"""

input_positive_gradient = set()
for string in variation_base["input_positive_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            input_positive_gradient.add(variation)
input_positive_gradient = sorted(input_positive_gradient)
"""Supported ``input_positive_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/input_positive_gradient.csv
"""

output_positive_gradient = set()
for string in variation_base["output_positive_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            output_positive_gradient.add(variation)
output_positive_gradient = sorted(output_positive_gradient)
"""Supported ``output_positive_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/output_positive_gradient.csv
"""

positive_gradient_costs = set()
for string in variation_base["positive_gradient_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            positive_gradient_costs.add(variation)
positive_gradient_costs = sorted(positive_gradient_costs)
"""Supported ``positive_gradient_costs`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/positive_gradient_costs.csv
"""

negative_gradient = set()
for string in variation_base["negative_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            negative_gradient.add(variation)
negative_gradient = sorted(negative_gradient)
"""Supported ``negative_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/negative_gradient.csv
"""

input_negative_gradient = set()
for string in variation_base["input_negative_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            input_negative_gradient.add(variation)
input_negative_gradient = sorted(input_negative_gradient)
"""Supported ``input_negative_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/input_negative_gradient.csv
"""

output_negative_gradient = set()
for string in variation_base["output_negative_gradient"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            output_negative_gradient.add(variation)
output_negative_gradient = sorted(output_negative_gradient)
"""Supported ``output_negative_gradient`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/output_negative_gradient.csv
"""

negative_gradient_costs = set()
for string in variation_base["negative_gradient_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            negative_gradient_costs.add(variation)
negative_gradient_costs = sorted(negative_gradient_costs)
"""Supported ``negative_gradient_costs`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/negative_gradient_costs.csv
"""

# Energy System Component Identifiers

bus = set()
for string in variation_base["bus"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            bus.add(variation)
bus = sorted(bus)
"""Supported ``bus`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/bus.csv
"""

sink = set()
for string in variation_base["sink"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            sink.add(variation)
sink = sorted(sink)
"""Supported ``sink`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/sink.csv
"""

source = set()
for string in variation_base["source"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            source.add(variation)
source = sorted(source)
"""Supported ``source`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/source.csv
"""

storage = set()
for string in variation_base["storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            storage.add(variation)
storage = sorted(storage)
"""Supported ``storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/storage.csv
"""

transformer = set()
for string in variation_base["transformer"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            transformer.add(variation)
transformer = sorted(transformer)
"""Supported ``transformer`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/transformer.csv
"""

connector = set()
for string in variation_base["connector"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            connector.add(variation)
connector = sorted(connector)
"""Supported ``connector`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/connector.csv
"""

# Energy System Component Identifiers - Energy Carrier
commodity = set()
for string in variation_base["commodity"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            commodity.add(variation)
commodity = sorted(commodity)
"""Supported ``commodity`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/commodity.csv
"""

hardcoal = set()
for string in variation_base["hardcoal"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            hardcoal.add(variation)
hardcoal = sorted(hardcoal)
"""Supported ``hardcoal`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/hardcoal.csv
"""

lignite = set()
for string in variation_base["lignite"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            lignite.add(variation)
lignite = sorted(lignite)
"""Supported ``lignite`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/lignite.csv
"""

gas = set()
for string in variation_base["gas"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gas.add(variation)
gas = sorted(gas)
"""Supported ``gas`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/gas.csv
"""

nuclear = set()
for string in [
    "nuclear",
    "atomic",
    "uranium",
]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            nuclear.add(variation)
nuclear = sorted(nuclear)
"""Supported ``nuclear`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/nuclear.csv
"""

oil = set()
for string in variation_base["oil"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            oil.add(variation)
oil = sorted(oil)
"""Supported ``oil`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/oil.csv
"""

solar = set()
for string in variation_base["solar"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            solar.add(variation)
solar = sorted(solar)
"""Supported ``solar`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/solar.csv
"""

wind = set()
for string in variation_base["wind"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            wind.add(variation)
wind = sorted(wind)
"""Supported ``wind`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/wind.csv
"""

water = set()
for string in variation_base["water"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            water.add(variation)
water = sorted(water)
"""Supported ``water`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/water.csv
"""

hot_water = set()
for string in variation_base["hot_water"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            hot_water.add(variation)
hot_water = sorted(hot_water)
"""Supported ``hot_water`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/hot_water.csv
"""

steam = set()
for string in variation_base["steam"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            steam.add(variation)
steam = sorted(steam)
"""Supported ``steam`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/steam.csv
"""

biomass = set()
for string in variation_base["biomass"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            biomass.add(variation)
biomass = sorted(biomass)
"""Supported ``biomass`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/biomass.csv
"""

electricity = set()
for string in variation_base["electricity"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            electricity.add(variation)
electricity = sorted(electricity)
"""Supported ``electricity`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/electricity.csv
"""

# Energy System Component Identifiers - Sector
power = set()
for string in variation_base["power"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power.add(variation)
power = sorted(power)
"""Supported ``power`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/power.csv
"""

heat = set()
for string in variation_base["heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat.add(variation)
heat = sorted(heat)
"""Supported ``heat`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/heat.csv
"""

mobility = set()
for string in variation_base["mobility"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            mobility.add(variation)
mobility = sorted(mobility)
"""Supported ``mobility`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/mobility.csv
"""

coupled = set()
for string in variation_base["coupled"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            coupled.add(variation)
coupled = sorted(coupled)
"""Supported ``coupled`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/coupled.csv
"""

# Energy System Component Identifiers - Name
renewables = set()
for string in variation_base["renewables"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            renewables.add(variation)
renewables = sorted(renewables)
"""Supported ``renewables`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/renewables.csv
"""

photovoltaic = set()
for string in variation_base["photovoltaic"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            photovoltaic.add(variation)
photovoltaic = sorted(photovoltaic)
"""Supported ``photovoltaic`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/photovoltaic.csv
"""

solarthermal = set()
for string in variation_base["solarthermal"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            solarthermal.add(variation)
solarthermal = sorted(solarthermal)
"""Supported ``solarthermal`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/solarthermal.csv
"""

onshore = set()
for string in variation_base["onshore"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            onshore.add(variation)
onshore = sorted(onshore)
"""Supported ``onshore`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/onshore.csv
"""

offshore = set()
for string in variation_base["offshore"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            offshore.add(variation)
offshore = sorted(offshore)
"""Supported ``offshore`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/offshore.csv
"""

hydro_electric = set()
for string in variation_base["hydro_electric"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            hydro_electric.add(variation)
hydro_electric = sorted(hydro_electric)
"""Supported ``hydro_electric`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/hydro_electric.csv
"""

mimo_transformer = set()
for string in variation_base["mimo_transformer"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            mimo_transformer.add(variation)
mimo_transformer = sorted(mimo_transformer)
"""Supported ``mimo_transformer`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/mimo_transformer.csv
"""

sito_flex_transformer = set()
for string in variation_base["sito_flex_transformer"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            sito_flex_transformer.add(variation)
sito_flex_transformer = sorted(sito_flex_transformer)
"""Supported ``sito_flex_transformer`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/sito_flex_transformer.csv
"""

generic_chp = set()
for string in variation_base["generic_chp"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            generic_chp.add(variation)
generic_chp = sorted(generic_chp)
"""Supported ``generic_chp`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/generic_chp.csv
"""

siso_nonlinear_transformer = set()
for string in variation_base["siso_nonlinear_transformer"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            siso_nonlinear_transformer.add(variation)
siso_nonlinear_transformer = sorted(siso_nonlinear_transformer)
"""Supported ``siso_nonlinear_transformer`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/siso_nonlinear_transformer.csv
"""

combined_heat_power = set()
for string in variation_base["combined_heat_power"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            combined_heat_power.add(variation)
combined_heat_power = sorted(combined_heat_power)
"""Supported ``combined_heat_power`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/combined_heat_power.csv
"""

power_plant = set()
for string in variation_base["power_plant"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power_plant.add(variation)
power_plant = sorted(power_plant)
"""Supported ``power_plant`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/power_plant.csv
"""

heat_plant = set()
for string in variation_base["heat_plant"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            heat_plant.add(variation)
heat_plant = sorted(heat_plant)
"""Supported ``heat_plant`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/heat_plant.csv
"""

electrical_line = set()
for string in variation_base["electrical_line"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            electrical_line.add(variation)
electrical_line = sorted(electrical_line)
"""Supported ``electrical_line`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/electrical_line.csv
"""

gas_station = set()
for string in variation_base["gas_station"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gas_station.add(variation)
gas_station = sorted(gas_station)
"""Supported ``gas_station`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/gas_station.csv
"""

gas_pipeline = set()
for string in variation_base["gas_pipeline"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gas_pipeline.add(variation)
gas_pipeline = sorted(gas_pipeline)
"""Supported ``gas_pipeline`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/gas_pipeline.csv
"""

gas_delivery = set()
for string in variation_base["gas_delivery"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            gas_delivery.add(variation)
gas_delivery = sorted(gas_delivery)
"""Supported ``gas_delivery`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/gas_delivery.csv
"""

oil_pipeline = set()
for string in variation_base["oil_pipeline"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            oil_pipeline.add(variation)
oil_pipeline = sorted(oil_pipeline)
"""Supported ``oil_pipeline`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/oil_pipeline.csv
"""

oil_delivery = set()
for string in variation_base["oil_delivery"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            oil_delivery.add(variation)
oil_delivery = sorted(oil_delivery)
"""Supported ``oil_delivery`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/oil_delivery.csv
"""

generic_storage = set()
for string in variation_base["generic_storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            generic_storage.add(variation)
generic_storage = sorted(generic_storage)
"""Supported ``generic_storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/generic_storage.csv
"""

hydro_electrical_storage = set()
for string in variation_base["hydro_electrical_storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            hydro_electrical_storage.add(variation)
hydro_electrical_storage = sorted(hydro_electrical_storage)
"""Supported ``hydro_electrical_storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/hydro_electrical_storage.csv
"""

electro_chemical_storage = set()
for string in variation_base["electro_chemical_storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            electro_chemical_storage.add(variation)
electro_chemical_storage = sorted(electro_chemical_storage)
"""Supported ``electro_chemical_storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/electro_chemical_storage.csv
"""

electro_mechanical_storage = set()
for string in variation_base["electro_mechanical_storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            electro_mechanical_storage.add(variation)
electro_mechanical_storage = sorted(electro_mechanical_storage)
"""Supported ``electro_mechanical_storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/electro_mechanical_storage.csv
"""

thermal_energy_storage = set()
for string in variation_base["thermal_energy_storage"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            thermal_energy_storage.add(variation)
thermal_energy_storage = sorted(thermal_energy_storage)
"""Supported ``thermal_energy_storage`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/thermal_energy_storage.csv
"""

power2x = set()
for string in variation_base["power2x"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power2x.add(variation)
power2x = sorted(power2x)
"""Supported ``power2x`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/power2x.csv
"""

power2heat = set()
for string in variation_base["power2heat"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            power2heat.add(variation)
power2heat = sorted(power2heat)
"""Supported ``power2heat`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/power2heat.csv
"""

imported = set()
for string in variation_base["imported"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            imported.add(variation)
imported = sorted(imported)
"""Supported ``imported`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/imported.csv
"""

backup = set()
for string in variation_base["backup"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            backup.add(variation)
backup = sorted(backup)
"""Supported ``backup`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/backup.csv
"""

demand = set()
for string in variation_base["demand"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            demand.add(variation)
demand = sorted(demand)
"""Supported ``demand`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/demand.csv
"""

export = set()
for string in variation_base["export"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            export.add(variation)
export = sorted(export)
"""Supported ``export`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/export.csv
"""

excess = set()
for string in variation_base["excess"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            excess.add(variation)
excess = sorted(excess)
"""Supported ``excess`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/excess.csv
"""


already_installed = set()
for string in variation_base["already_installed"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            already_installed.add(variation)
already_installed = sorted(already_installed)
"""Supported ``already_installed`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/already_installed.csv
"""

milp = set()
for string in variation_base["milp"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            milp.add(variation)
milp = sorted(milp)
"""Supported ``milp`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/milp.csv
"""

startup_costs = set()
for string in variation_base["startup_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            startup_costs.add(variation)
startup_costs = sorted(startup_costs)
"""Supported ``startup_costs`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/startup_costs.csv
"""

shutdown_costs = set()
for string in variation_base["shutdown_costs"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            shutdown_costs.add(variation)
shutdown_costs = sorted(shutdown_costs)
"""Supported ``shutdown_costs`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/shutdown_costs.csv
"""

minimum_uptime = set()
for string in variation_base["minimum_uptime"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_uptime.add(variation)
minimum_uptime = sorted(minimum_uptime)
"""Supported ``minimum_uptime`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_uptime.csv
"""

minimum_downtime = set()
for string in variation_base["minimum_downtime"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            minimum_downtime.add(variation)
minimum_downtime = sorted(minimum_downtime)
"""Supported ``minimum_downtime`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/minimum_downtime.csv
"""

initial_status = set()
for string in variation_base["initial_status"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            initial_status.add(variation)
initial_status = sorted(initial_status)
"""Supported ``initial_status`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/initial_status.csv
"""

initial_soc = set()
for string in variation_base["initial_soc"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            initial_soc.add(variation)
initial_soc = sorted(initial_soc)
"""Supported ``initial_soc`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/initial_soc.csv
"""

exogenously_set = set()
for string in variation_base["exogenously_set"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            exogenously_set.add(variation)
exogenously_set = sorted(exogenously_set)
"""Supported ``exogenously_set`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/exogenously_set.csv
"""

exogenously_set_value = set()
for string in variation_base["exogenously_set_value"]:
    for sep in seperators:
        for variation in strutils.variate_compounds(string, stitch_with=sep):
            exogenously_set_value.add(variation)
exogenously_set_value = sorted(exogenously_set_value)
"""Supported ``exogenously_set_value`` spellings.

.. csv-table::
   :file: docs/source/csvs/spellings/exogenously_set_value.csv
"""

energy_system_component_identifiers = nts.NodeColorGroupings(
    component=collections.OrderedDict(
        [
            ("bus", bus),
            ("combined_heat_power", combined_heat_power),
            ("sink", sink),
            ("storage", storage),
            ("source", source),
            ("transformer", transformer),
            ("connector", connector),
        ]
    ),
    carrier=collections.OrderedDict(
        [
            ("hardcoal", hardcoal),
            ("lignite", lignite),
            ("gas", gas),
            ("nuclear", nuclear),
            ("oil", oil),
            ("solar", solar),
            ("wind", wind),
            ("water", water),
            ("hot_water", hot_water),
            ("steam", steam),
            ("biomass", biomass),
            ("electricity", electricity),
        ]
    ),
    sector=collections.OrderedDict(
        [
            ("power", power),
            ("heat", heat),
            ("mobility", mobility),
            ("coupled", coupled),
        ]
    ),
    name=collections.OrderedDict(
        [
            ("photovoltaic", photovoltaic),
            ("solarthermal", solarthermal),
            ("onshore", onshore),
            ("offshore", offshore),
            ("hydro_electric", hydro_electric),
            ("combined_heat_power", combined_heat_power),
            ("power_plant", power_plant),
            ("heat_plant", heat_plant),
            ("electrical_line", electrical_line),
            ("gas_pipeline", gas_pipeline),
            ("gas_delivery", gas_delivery),
            ("oil_pipeline", oil_pipeline),
            ("oil_delivery", oil_delivery),
            ("hydro_electrical_storage", hydro_electrical_storage),
            ("electro_chemical_storage", electro_chemical_storage),
            ("electro_mechanical_storage", electro_mechanical_storage),
            ("thermal_energy_storage", thermal_energy_storage),
            ("power2x", power2x),
            ("power2heat", power2heat),
            ("imported", imported),
            ("backup", backup),
            ("demand", demand),
            ("export", export),
            ("excess", excess),
        ]
    ),
)
"""Recognized node name representations."""


# def to_csv(iterable, name, columns=4, path=None, **kwargs):
#     """ Store an :paramref:`~to_csv.iterable` under
#     :paramref:`name.csv <to_csv.name>` having n :paramref:`~to_csv.columns` in
#     ``tessif/frused/spellings/name.csv``.

#     Parameters
#     ----------
#     iterable: :class:`~collections.abc.Iterable`
#         The iterable used for constructing the csv table.

#     name: str
#         Table is stored in
#         ``tessif/../doc/docs/source/csvs/spellings/name.csv``

#     columns: int, default=4
#         Number of columns the csv table will have

#     path: str, default=None
#         String representation of the path the csv is written
#         to. Default of ``None`` translates to::

#             tessif_doc/docs/source/csvs/spellings/name.csv

#     kwargs:
#         kwargs are passed to `pandas.DataFrame.to_csv
#         <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html>`_

#         Note
#         ----
#         ``index`` and ``header`` are set to ``False`` by default. Provide
#         parameters for overriding those if needed.
#     """

#     defaults = {
#         'index': False,
#         'header': False,
#     }

#     # handle kwargs and defaults
#     for k, v in defaults.items():
#         if k not in kwargs:
#             kwargs.update({k: v})

#     # construct data frame having 4 columns
#     df = pd.DataFrame(list(zip(*ittools.group(iterable, columns))))

#     # path relative to tessif's installation
#     if path is None:
#         path = os.path.join(
#             doc_dir, 'source', 'api', 'frused',
#             'spellings', '{}.csv'.format(name))

#     # write df to csv
#     df.to_csv(path_or_buf=path, **kwargs)


def get_from(dct, smth_like, dflt=None):
    """Map different spellings of the same string key to one specific spelling.

    Get :paramref:`~get_from.smth_like` from the string keyed
    :paramref:`~get_from.dct` otherwise return :paramref:`~get_from.dflt`.

    Used through out tessif to allow a wide variaty of string mappings for
    descibing the same thing. Whenn accessing (somewhat) unknown or unfamiliar
    input data sources.

    Parameters
    ----------
    dct: dict
        Dictionairy to key key with something that looks like
        :paramref:`~get_from.smth_like`

    smth_like: str
        string representation of a key of which an identically named attribute
        is to be found in :mod:`tessif.frused.spellings`.

    dflt: value, default=None,
        value to return when no appropriate spelling exists in
        :mod:`tessif.frused.spellings` or no spelling variation of this key is
        present in :paramref:`~get_from.dct`

    Note
    ----
    A detailed debugging log is created to help with this sometimes error prone
    approach to allow arbitrarily many spellings for the same set of data.

    All logs can be found in ``tessif.write.logs``

    The logging level can be tweaked using
    :attr:`configurations.spellings_logging_level
    <tessif.frused.configurations.spellings_logging_level>`.

    Examples
    --------
    Design Case:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(get_from(lookup, smth_like='emissions'))
    10

    Unsuccessful matching between spellings variation and dict keys:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(get_from(lookup, smth_like='timeindex', dflt='Failed'))
    Failed

    Unsuccessful matching between smth_like and hardcoded mappings:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(get_from(lookup, smth_like='co2_emissions', dflt='42'))
    42
    """
    log_level = logging.DEBUG

    getattr(logger, log_level)(50 * "-")
    getattr(logger, log_level)(f"Try getting a key similar to {smth_like}...")

    if smth_like in globals():

        getattr(logger, log_level)('... found a "many->one" spellings key mapping...')
        getattr(logger, log_level)("... trying to match a key ...")

        for variation in globals()[smth_like]:
            if variation in dct.keys():
                getattr(logger, log_level)(f"... found {variation}...")
                getattr(logger, log_level)(f"... which matches to {dct[variation]}")
                getattr(logger, log_level)(50 * "-")
                return dct[variation]

        else:
            msg = (
                f'None of the spellings for "{smth_like}" could be matched'
                + f' to "{dct.keys()}". Returning "{dflt}"'
            )

            getattr(logger, log_level)(msg)
            getattr(logger, log_level)(50 * "-")
            return dflt
    else:
        msg = (
            f'No "many->one" spellings key mapping found for "{smth_like}".'
            + f' Returning "{dflt}"'
        )
        getattr(logger, log_level)(msg)
        logger.debug(50 * "-")
        return dflt


def match_key_from(mppng, smth_like, dflt=None):
    """
    Find out wich particular spelling variation was used for string keying.

    Match a key from :paramref:`~match_key_from.smth_like` to
    :paramref:`~match_key_from.mppng` otherwise return
    :paramref:`~match_key_from.dflt`.

    Used through out tessif to allow a wide variaty of string mappings for
    descibing the same thing. Whenn accessing (somewhat) unknown or unfamiliar
    input data sources. And the exact key is needed. (i.e in
    :meth:`tessif.parse.xl_like`)


    Parameters
    ----------
    mppng: dict
        Mapping of which a string key is to be found that looks like
        :paramref:`~match_key_from.smth_like`

    smth_like: str
        string representation of a key of which an identically named attribute
        is to be found in :mod:`tessif.frused.spellings`.
        (i.e, if your key is ``label`` this argument has to be ``name`` since
        :mod:`~tessif.frused.spellings` maps ``label`` to
        :attr:`~tessif.frused.spellings.name`)

    dflt: value, default=None,
        value to return when no appropriate spelling exists in
        :mod:`tessif.frused.spellings` or no spelling variation of this key is
        present in :paramref:`~match_key_from.mppng`

    Note
    ----
    A detailed debugging log is created to help with this sometimes error prone
    approach to allow arbitrarily many spellings for the same set of data.

    All logs can be found in ``tessif.write.logs``

    The logging level can be tweaked using
    :attr:`configurations.spellings_logging_level
    <tessif.frused.configurations.spellings_logging_level>`.

    Examples
    --------
    Design Case:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(match_key_from(lookup, smth_like='emissions'))
    CO2 Emissions

    Unsuccessful matching between spellings variation and mapping keys:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(match_key_from(lookup, smth_like='timeindex', dflt='Failed'))
    Failed

    Unsuccessful matching between smth_like and hardcoded mappings:

    >>> from tessif.frused import spellings
    >>> lookup = {'CO2 Emissions': 10,}
    >>> print(match_key_from(lookup, smth_like='random_key', dflt='42'))
    42
    """
    log_level = logging.DEBUG

    logger.debug(50 * "-")
    logger.debug(f"Try getting a key similiar to {smth_like}...")

    if smth_like in globals():

        logger.debug('... found a "many->one" spellings7 key mapping...')
        logger.debug("... trying to match a key ...")

        for variation in globals()[smth_like]:
            if variation in mppng.keys():
                logger.debug(f"... found {variation}")
                logger.debug(50 * "-")
                return variation

        else:
            msg = (
                f'None of the spellings for "{smth_like}" could be matched'
                + f' to "{mppng.keys()}". Returning "{dflt}"'
            )

            getattr(logger, log_level)(msg)
            logger.debug(50 * "-")
            return dflt
    else:
        msg = (
            f'No "many->one" spellings key mapping found for "{smth_like}".'
            + f' Returning "{dflt}"'
        )
        getattr(logger, log_level)(msg)
        logger.debug(50 * "-")
        return dflt
