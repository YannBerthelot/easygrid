"""
'Realistic' config to be used for testing
"""
from functools import partial

import numpy as np

from easygrid.math_utils import get_hourly_variation
from easygrid.types import (
    BatteryConfig,
    GridConfig,
    LoadConfig,
    MicrogridConfig,
    PvConfig,
)

CAPACITY = 1e5
MAX_TIMESTEP = int(1e3)

battery_config: BatteryConfig = {
    "capacity": CAPACITY,
    "high_capacity": 0.8 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": 100,
    "min_output": 20,
    "initial_energy": 0.2 * CAPACITY,
    "overcharge_penalty": 1,
}

day_variation = partial(
    get_hourly_variation, period=24, time_max=15, time_min=3, size=MAX_TIMESTEP
)
grid_config: GridConfig = {
    "import_prices": list(i for i in day_variation(max_val=10, min_val=6)),
    "export_prices": list(i for i in day_variation(max_val=5, min_val=1)),
}
pv_config: PvConfig = {
    "pv_production_ts": list(
        min(0, i + np.random.randint(low=-100, high=0))
        for i in get_hourly_variation(
            max_val=100,
            min_val=50,
            period=24,
            time_max=12,
            time_min=0,
            size=MAX_TIMESTEP,
        )
    ),
}

load_config: LoadConfig = {
    "load_ts": list(
        min(0, i + np.random.randint(low=-500, high=0))
        for i in get_hourly_variation(
            max_val=1000,
            min_val=300,
            period=24,
            time_max=12,
            time_min=0,
            size=MAX_TIMESTEP,
        )
    ),
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
