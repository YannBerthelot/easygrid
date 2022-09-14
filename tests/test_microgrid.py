import copy
import os
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from easygrid.__main__ import main
from easygrid.config.pymgrid_config import (
    MAX_TIMESTEP,
    battery_config,
    grid_config,
    load_config,
    mg_config,
    pv_config,
)
from easygrid.microgrid import Battery, Grid, Load, Microgrid, Photovoltaic
from easygrid.types import GridConfig, LoadConfig, PvConfig

battery = 1000
grid = 1000
action = np.array([battery, grid])


@patch("matplotlib.pyplot.show")  # used to prevent displaying plots
def test_main(mock_show):
    main()  # includes testing show logs


def test_microgrid():
    mg = Microgrid(mg_config)
    mg.run_timestep(action, logging=True)
    mg.run_timestep(action, logging=False)
    with pytest.raises(NotImplementedError):
        mg.print_info()

    faulty_import = os.path.join(os.path.dirname(__file__), "faulty_import.csv")
    pd.Series(np.random.randint(5, size=MAX_TIMESTEP - 5)).to_csv(
        faulty_import, index=False
    )
    faulty_export = os.path.join(os.path.dirname(__file__), "faulty_export.csv")
    pd.Series(np.random.randint(5, size=MAX_TIMESTEP - 5)).to_csv(
        faulty_export, index=False
    )
    faulty_grid_config = GridConfig.parse_obj(
        {
            "import_prices": faulty_import,
            "export_prices": faulty_export,
        }
    )

    faulty_config = copy.deepcopy(mg_config)
    faulty_config.grid = faulty_grid_config
    with pytest.raises(ValueError):
        faulty_mg = Microgrid(faulty_config)

    faulty_pv_config = PvConfig.parse_obj(
        {
            "pv_production_ts": faulty_import,
        }
    )
    faulty_config = copy.deepcopy(mg_config)
    faulty_config.pv = faulty_pv_config
    with pytest.raises(ValueError):
        faulty_mg = Microgrid(faulty_config)
        faulty_mg
    pd.Series([1, 1]).to_csv("faulty_load.csv", index=False)
    faulty_load_config = LoadConfig.parse_obj(
        {
            "load_ts": "faulty_load.csv",
        }
    )
    faulty_config = copy.deepcopy(mg_config)
    faulty_config.load = faulty_load_config
    with pytest.raises(ValueError):
        faulty_mg = Microgrid(faulty_config)
        faulty_mg

    mg.get_error_cost(-1000)  # test error cost computation for negative energy
    mg.get_error_cost(1000)  # test error cost computation for positive energy
    mg.log_energies(1, 1, 1, 1)  # test auto balance computation
    figs = mg.show_logs(show=False)
    assert figs is not None
    assert mg.config is not None
    duration = 10
    mg.set_battery_from_duration(duration)
    assert mg.battery.capacity == mg.load.__mean__ * duration
    mg.reset()
    assert mg.t == 0
    mg.reset(reset_logs=True)
    assert len(mg.costs["overcharge"]) == 0
    # check that config file is created
    config_file_name = os.path.join(os.path.dirname(__file__), "config.json")
    mg.save_config(config_file_name)
    assert os.path.exists(config_file_name)
    for file in ["faulty_load.csv", faulty_export, faulty_import, config_file_name]:
        os.remove(file)

    # Test scaler
    assert (
        mg.scale_action(-1, mg.max_actions[0], mg.min_actions[0]) == mg.min_actions[0]
    )
    assert mg.scale_action(1, mg.max_actions[0], mg.min_actions[0]) == mg.max_actions[0]


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
    assert battery.config is not None


def test_grid():
    grid = Grid(grid_config)
    assert grid.get_cost(energy=1e3, t=np.random.randint(grid.__len__)) >= 0
    assert grid.get_cost(energy=-1e3, t=np.random.randint(grid.__len__)) <= 0
    assert grid.get_cost(energy=0, t=np.random.randint(grid.__len__)) == 0
    faulty_import = os.path.join(os.path.dirname(__file__), "faulty_import.csv")
    pd.Series(np.random.randint(5, size=MAX_TIMESTEP)).to_csv(
        faulty_import, index=False
    )
    faulty_export = os.path.join(os.path.dirname(__file__), "faulty_export.csv")
    pd.Series(np.random.randint(5, size=MAX_TIMESTEP - 1)).to_csv(
        faulty_export, index=False
    )
    faulty_config = GridConfig.parse_obj(
        {
            "import_prices": faulty_import,
            "export_prices": faulty_export,
        }
    )
    with pytest.raises(ValueError):
        faulty_grid = Grid(faulty_config)
        faulty_grid
    os.remove(faulty_import)
    os.remove(faulty_export)
    assert grid.config is not None


def test_pv():
    pv = Photovoltaic(pv_config)
    pv.get_power(np.random.randint(pv.__len__))
    assert pv.config is not None
    assert pv.__mean__ > 0


def test_load():
    load = Load(load_config)
    load.get_load(np.random.randint(load.__len__))
    assert load.config is not None
