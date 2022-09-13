"""
'Realistic' config to be used for testing
"""
import os

import numpy as np

from easygrid.data.data_utils import DATA_FOLDER, get_indexes, load_data
from easygrid.types import (
    BatteryConfig,
    GridConfig,
    LoadConfig,
    MicrogridConfig,
    PvConfig,
)

INDEXES = get_indexes(DATA_FOLDER)
LOAD = load_data(
    INDEXES["load"][3]
)  # RefBldgPrimarySchoolNew2004_v1.3_7.1_2A_USA_TX_HOUSTON.csv
DURATION = 10
CAPACITY = int(np.mean(LOAD) * DURATION)
MAX_TIMESTEP = 8760

load_file = os.path.join(
    os.path.join(DATA_FOLDER, "load"),
    "RefBldgPrimarySchoolNew2004_v1.3_7.1_2A_USA_TX_HOUSTON.csv",
)
pv_file = os.path.join(os.path.join(DATA_FOLDER, "pv"), "Houston_722430TYA.csv")
import_price_file = os.path.join(
    os.path.join(DATA_FOLDER, "prices"), "import_prices_artificial.csv"
)
export_price_file = os.path.join(
    os.path.join(DATA_FOLDER, "prices"), "export_prices_artificial.csv"
)
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
        "pv_production_ts": pv_file,
    }
)

grid_config = GridConfig.parse_obj(
    {
        "import_prices": import_price_file,
        "export_prices": export_price_file,
    }
)

load_config = LoadConfig.parse_obj(
    {
        "load_ts": load_file,
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
