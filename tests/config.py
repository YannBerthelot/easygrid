import numpy as np

from easygrid.types import (
    Action,
    BatteryConfig,
    GridConfig,
    LoadConfig,
    MicrogridConfig,
    PvConfig,
)

action = Action.parse_obj({"battery": 1000, "grid": 1000})

CAPACITY = 1e5
MAX_TIMESTEP = int(1e3)

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

grid_config = GridConfig.parse_obj(
    {
        "import_prices": np.random.randint(5, size=MAX_TIMESTEP),
        "export_prices": np.random.randint(5, size=MAX_TIMESTEP),
        "import_price_factor": 1.5,
        "export_price_factor": 1.2,
    }
)

pv_config = PvConfig.parse_obj(
    {
        "pv_production_ts": np.random.randint(5, size=MAX_TIMESTEP),
        "production_factor": 1.1,
    }
)

load_config = LoadConfig.parse_obj(
    {
        "load_ts": np.random.randint(5, size=MAX_TIMESTEP),
        "load_factor": 2.1,
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
