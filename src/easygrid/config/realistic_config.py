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
MAX_TIMESTEP = 8760

battery_config = BatteryConfig.parse_obj(
    {
        "capacity": CAPACITY,
        "high_capacity": 0.8 * CAPACITY,
        "low_capacity": 0.2 * CAPACITY,
        "max_output": 100,
        "min_output": 20,
        "initial_energy": 0.2 * CAPACITY,
        "overcharge_penalty": 1,
    }
)

day_variation = partial(
    get_hourly_variation, period=24, time_max=15, time_min=3, size=MAX_TIMESTEP
)
grid_config = GridConfig.parse_obj(
    {
        "import_prices": np.array(
            list(i for i in day_variation(max_val=10, min_val=6))
        ),
        "export_prices": np.array(list(i for i in day_variation(max_val=5, min_val=1))),
    }
)
pv_config = PvConfig.parse_obj(
    {
        "pv_production_ts": np.array(
            list(
                min(0, i + np.random.randint(low=-100, high=0))
                for i in get_hourly_variation(
                    max_val=100,
                    min_val=50,
                    period=24,
                    time_max=12,
                    time_min=0,
                    size=MAX_TIMESTEP,
                )
            )
        ),
    }
)

load_config = LoadConfig.parse_obj(
    {
        "load_ts": np.array(
            list(
                min(0, i + np.random.randint(low=-500, high=0))
                for i in get_hourly_variation(
                    max_val=1000,
                    min_val=300,
                    period=24,
                    time_max=12,
                    time_min=0,
                    size=MAX_TIMESTEP,
                )
            )
        ),
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
