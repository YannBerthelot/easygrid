import pytest

from easygrid.microgrid import Action, Battery, Microgrid

CAPACITY = 1e5
battery_config = {
    "capacity": CAPACITY,
    "high_capacity": 0.8 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": 100,
    "min_output": 20,
    "initial_energy": 0.2 * CAPACITY,
}
action: Action = {"battery": 1000, "grid": 1000}


def test_microgrid():
    config = {"BATTERY": battery_config}
    mg = Microgrid(config)
    with pytest.raises(NotImplementedError):
        mg.run_timestep(action)
    with pytest.raises(NotImplementedError):
        mg.print_info()
    with pytest.raises(NotImplementedError):
        mg.reset()


def test_battery():
    battery = Battery(battery_config)
    battery.charge(1000)
    battery.discharge(1000)
    with pytest.raises(ValueError):
        battery.charge(-1000)
    with pytest.raises(ValueError):
        battery.discharge(-1000)
    battery.process_action(action["battery"])
    battery.process_action(-action["battery"])
    assert (
        isinstance(battery.state_of_charge, float)
        and (battery.state_of_charge >= 0)
        and (battery.state_of_charge <= 1)
    )
    assert isinstance(battery.energy, float) and (battery.energy >= 0)
    with pytest.raises(AssertionError):
        battery._energy = -1
        battery.energy
