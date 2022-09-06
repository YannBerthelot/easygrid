"""
'Realistic' config to be used for testing
"""
import numpy as np

from easygrid.data.data_utils import DATA_FOLDER, get_indexes
from easygrid.math_utils import get_hourly_variation
from easygrid.types import (
    BatteryConfig,
    GridConfig,
    LoadConfig,
    MicrogridConfig,
    PvConfig,
)

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

grid_config: GridConfig = {
    "import_prices": list(
        i
        for i in get_hourly_variation(
            max_val=10, min_val=6, period=24, time_max=15, time_min=3, size=MAX_TIMESTEP
        )
    ),
    "export_prices": list(
        i
        for i in get_hourly_variation(
            max_val=5, min_val=1, period=24, time_max=15, time_min=3, size=MAX_TIMESTEP
        )
    ),
}
pv_config: PvConfig = {
    "pv_production_ts": PV,
}

load_config: LoadConfig = {
    "load_ts": LOAD,
}
mg_config: MicrogridConfig = {
    "max_timestep": MAX_TIMESTEP,
    "overprod_penalty": 1,
    "underprod_penalty": 1,
}
config = {
    "BATTERY": battery_config,
    "MICROGRID": mg_config,
    "GRID": grid_config,
    "PV": pv_config,
    "LOAD": load_config,
}
