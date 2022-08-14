import numpy as np

from easygrid.types import Action, BatteryConfig, GridConfig, LoadConfig, PvConfig

CAPACITY = 1e5
MAX_TIMESTEP = int(1e3)
battery_config: BatteryConfig = {
    "capacity": CAPACITY,
    "high_capacity": 0.8 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": 100,
    "min_output": 20,
    "initial_energy": 0.2 * CAPACITY,
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

config = {
    "BATTERY": battery_config,
    "MICROGRID": {"MAX_TIMESTEP": MAX_TIMESTEP},
    "GRID": grid_config,
    "PV": pv_config,
}
