import copy

import numpy as np
import pytest

from easygrid.microgrid import Battery, Grid, Microgrid, Photovoltaic
from easygrid.types import GridConfig

from .config import MAX_TIMESTEP, action, battery_config, config, grid_config, pv_config


def test_microgrid():
    mg = Microgrid(config)
    mg.run_timestep(action)
    with pytest.raises(NotImplementedError):
        mg.print_info()
    with pytest.raises(NotImplementedError):
        mg.reset()
    faulty_grid_config: GridConfig = {
        "import_prices": np.random.randint(5, size=MAX_TIMESTEP - 1),
        "export_prices": np.random.randint(5, size=MAX_TIMESTEP - 1),
    }
    faulty_config = copy.deepcopy(config)
    faulty_config["GRID"] = faulty_grid_config
    with pytest.raises(ValueError):
        faulty_mg = Microgrid(faulty_config)
        faulty_mg

    faulty_pv_config: GridConfig = {
        "pv_production_ts": np.random.randint(5, size=MAX_TIMESTEP - 1),
    }
    faulty_config = copy.deepcopy(config)
    faulty_config["PV"] = faulty_pv_config
    with pytest.raises(ValueError):
        faulty_mg = Microgrid(faulty_config)
        faulty_mg


def test_battery():
    battery = Battery(battery_config)
    battery.charge_discharge(1000)
    battery.charge_discharge(-1000)
    assert (
        isinstance(battery.state_of_charge, float)
        and (battery.state_of_charge >= 0)
        and (battery.state_of_charge <= 1)
    )
    battery.charge_discharge(1e8)
    assert (
        isinstance(battery.state_of_charge, float)
        and (battery.state_of_charge >= 0)
        and (battery.state_of_charge <= 1)
    )
    battery.charge_discharge(-2e8)
    assert (
        isinstance(battery.state_of_charge, float)
        and (battery.state_of_charge >= 0)
        and (battery.state_of_charge <= 1)
    )
    assert isinstance(battery.energy, float) and (battery.energy >= 0)
    with pytest.raises(ValueError):
        battery._energy = -1
        battery.energy


def test_grid():
    grid = Grid(grid_config)
    assert grid.get_cost(energy=1e3, t=np.random.randint(grid.__len__)) >= 0
    assert grid.get_cost(energy=-1e3, t=np.random.randint(grid.__len__)) <= 0
    assert grid.get_cost(energy=0, t=np.random.randint(grid.__len__)) == 0
    faulty_config: GridConfig = {
        "import_prices": np.random.randn(MAX_TIMESTEP),
        "export_prices": np.random.randn(MAX_TIMESTEP - 1),
    }
    with pytest.raises(ValueError):
        faulty_grid = Grid(faulty_config)
        faulty_grid


def test_pv():
    pv = Photovoltaic(pv_config)
    pv.get_power(np.random.randint(pv.__len__))
