import pytest

from easygrid.env import GridEnv
from easygrid.types import MicrogridConfig

from .config import action, mg_config


def test_env():
    env = GridEnv(mg_config)
    assert len(env.step(action)) == 4
    assert len(env.reset()) > 0
    assert isinstance(env.config, MicrogridConfig)
    with pytest.raises(NotImplementedError):
        env.render()
    with pytest.raises(NotImplementedError):
        env.close()
