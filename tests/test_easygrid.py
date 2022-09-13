import pytest

from easygrid.config.pymgrid_config import mg_config
from easygrid.env import GridEnv
from easygrid.types import MicrogridConfig


def test_env():
    env = GridEnv(mg_config)
    assert len(env.step(env.action_space.sample())) == 4
    assert len(env.reset()) > 0
    assert isinstance(env.config, MicrogridConfig)
    with pytest.raises(NotImplementedError):
        env.render()
    with pytest.raises(NotImplementedError):
        env.close()

    done = False
    i = 1
    while not done:
        obs, reward, done, _ = env.step(env.action_space.sample())
        i += 1
    assert i == env.microgrid.__len__ - 1
