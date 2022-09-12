"""
'Realistic' config to be used for testing
"""
import numpy as np

from easygrid.config.realistic_config import grid_config
from easygrid.data.data_utils import DATA_FOLDER, get_indexes, load_data
from easygrid.types import BatteryConfig, LoadConfig, MicrogridConfig, PvConfig

INDEXES = get_indexes(DATA_FOLDER)
LOAD = load_data(
    INDEXES["load"][3]
)  # RefBldgPrimarySchoolNew2004_v1.3_7.1_2A_USA_TX_HOUSTON.csv
PV = load_data(INDEXES["pv"][0])
DURATION = 10
CAPACITY = int(np.mean(LOAD) * DURATION)  # Houston_722430TYA.csv
MAX_TIMESTEP = int(1e3)
battery_config = BatteryConfig.parse_obj(
    {
        "capacity": CAPACITY,
        "high_capacity": 0.9 * CAPACITY,
        "low_capacity": 0.2 * CAPACITY,
        "max_output": int(np.ceil(CAPACITY / DURATION)),
        "min_output": 0,
        "initial_energy": 0.2 * CAPACITY,
        "overcharge_penalty": 1,
    }
)

pv_config = PvConfig.parse_obj(
    {
        "pv_production_ts": PV,
    }
)

load_config = LoadConfig.parse_obj(
    {
        "load_ts": LOAD,
    }
)

mg_config = MicrogridConfig.parse_obj(
    {
        "max_timestep": MAX_TIMESTEP,
        "overprod_penalty": 1,
        "underprod_penalty": 1,
        "pv": pv_config,
        "load": load_config,
        "battery": battery_config,
        "grid": grid_config,
    }
)
