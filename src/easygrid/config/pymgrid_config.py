"""
'Realistic' config to be used for testing
"""
import numpy as np

from easygrid.config.realistic_config import grid_config, mg_config
from easygrid.data.data_utils import DATA_FOLDER, get_indexes
from easygrid.types import BatteryConfig, LoadConfig, PvConfig

INDEXES = get_indexes(DATA_FOLDER)
LOAD = INDEXES["load"][3]  # RefBldgPrimarySchoolNew2004_v1.3_7.1_2A_USA_TX_HOUSTON.csv
PV = INDEXES["pv"][0]
DURATION = 10
CAPACITY = int(np.mean(LOAD) * DURATION)  # Houston_722430TYA.csv
MAX_TIMESTEP = int(1e3)

battery_config: BatteryConfig = {
    "capacity": CAPACITY,
    "high_capacity": 0.9 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": int(np.ceil(CAPACITY / DURATION)),
    "min_output": 0,
    "initial_energy": 0.2 * CAPACITY,
    "overcharge_penalty": 1,
}

pv_config: PvConfig = {
    "pv_production_ts": PV,
}

load_config: LoadConfig = {
    "load_ts": LOAD,
}

config = {
    "BATTERY": battery_config,
    "MICROGRID": mg_config,
    "GRID": grid_config,
    "PV": pv_config,
    "LOAD": load_config,
}
