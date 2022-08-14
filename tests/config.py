import numpy as np

from easygrid.types import (
    Action,
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
action: Action = {"battery": 1000, "grid": 1000}

grid_config: GridConfig = {
    "import_prices": np.random.randint(5, size=MAX_TIMESTEP),
    "export_prices": np.random.randint(5, size=MAX_TIMESTEP),
}

pv_config: PvConfig = {
    "pv_production_ts": np.random.randint(5, size=MAX_TIMESTEP),
}

load_config: LoadConfig = {
    "load_ts": np.random.randint(5, size=MAX_TIMESTEP),
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
