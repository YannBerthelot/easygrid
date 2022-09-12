"""
This module creates the gym environment wrapped arround the microgrid core
"""

from abc import abstractmethod
from typing import Tuple

import gym
import numpy as np
from gym import spaces

from easygrid.microgrid import Microgrid
from easygrid.types import MicrogridConfig

# from gym import spaces


class GridEnv(gym.Env):
    """
    Gym Environment wrapper of the Microgrid env.

    ...

    Attributes
    ----------
    microgrid : easygrid.Microgrid
        The underlyind microgrid object which will actually handle the \
             computations. See this class for more details
    Methods
    -------
    step : executes the action given by the agent (or something else) and \
        returns information about the state of the environment and reward
    reset : resets the environment to an initial state and returns this state.
    render : displays the environment (not supported atm)
    close : TBD
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, config: MicrogridConfig) -> None:

        """
        Creates the relevant attributes based on the config

        Args:
            config (dict): Configuration for the underlying microgrid.
        """
        super().__init__()
        self.microgrid = Microgrid(config)
        self.observation_space = spaces.Box(
            low=self.microgrid.min_values,
            high=self.microgrid.max_values,
            dtype=np.float32,
        )
        self.action_space = spaces.Box(
            low=self.microgrid.min_actions,
            high=self.microgrid.max_actions,
            dtype=np.float32,
        )

    @property
    def config(self) -> MicrogridConfig:
        """
        Returns:
            MicrogridConfig: The current underlying config
        """
        return self.microgrid.config

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, str]:
        """
        Executes the action given by the agent (or something else) and \
        returns information about the state of the environment and reward

        Args:
            action (np.ndarray): The action to be processed by the environment,\
                 it should contain:
                - How much to store/discharge in the battery (float)
                - How much to sell/buy from the grid (float)

        Returns:
            Tuple[np.ndarray, float, bool, NoneType]: The observation, reward,\
                done and info following gym template
        """
        observation, done, costs = self.microgrid.run_timestep(action)
        reward = GridEnv.compute_reward(costs)
        info = ""
        return observation, reward, done, info

    def reset(self) -> np.ndarray:
        """
        Resets the environment to an initial state and returns this state.

        Raises:
            NotImplementedError: _description_
        """
        return self.microgrid.reset()

    def render(self, mode="human"):
        """TBD

        Args:
            mode (str, optional): _description_. Defaults to "human".

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def close(self):
        """
        TBD

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    @abstractmethod
    def compute_reward(costs: Tuple[float, float, float]) -> float:
        """
        Computes the reward/cost based on the precomputed costs.
        TBD : add the possibility to integrate the state of the microgrid

        Args:
            costs (Tuple[float, float, float]): The overcharge, grid and
                                                    error costs

        Returns:
            float: The reward/cost
        """
        reward = sum(costs)
        return reward
