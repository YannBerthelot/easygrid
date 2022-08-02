import pytest

from easygrid.microgrid import Action, Battery

CAPACITY = 1e5
battery_config = {
    "capacity": CAPACITY,
    "high_capacity": 0.8 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": 100,
    "low_output": 20,
}


def test_battery():
    battery = Battery(*battery_config.values())
    battery.charge(1000)
    battery.discharge(1000)
    with pytest.raises(ValueError):
        battery.charge(-1000)
        battery.discharge(-1000)
    action: Action = {"battery": 1000, "grid": 1000}
    battery.process_action(action["battery"])
