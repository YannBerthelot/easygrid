import pytest

from easygrid.env import GridEnv

from .config import action, mg_config


def test_env():
    env = GridEnv(mg_config)
    env.step(action)
    with pytest.raises(NotImplementedError):
        env.reset()
    with pytest.raises(NotImplementedError):
        env.render()
    with pytest.raises(NotImplementedError):
        env.close()
