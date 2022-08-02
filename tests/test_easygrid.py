import pytest

from easygrid import __version__
from easygrid.env import GridEnv
from easygrid.microgrid import Action

CAPACITY = 1e5
battery_config = {
    "capacity": CAPACITY,
    "high_capacity": 0.8 * CAPACITY,
    "low_capacity": 0.2 * CAPACITY,
    "max_output": 100,
    "min_output": 20,
    "initial_energy": 0.2 * CAPACITY,
}
config = {"BATTERY": battery_config}
action: Action = {"battery": 1000, "grid": 1000}


def test_env():
    env = GridEnv(config)
    with pytest.raises(NotImplementedError):
        env.step(action)
    with pytest.raises(NotImplementedError):
        env.reset()
    with pytest.raises(NotImplementedError):
        env.render()
    with pytest.raises(NotImplementedError):
        env.close()


def test_version():
    assert __version__ == "0.1.0"
