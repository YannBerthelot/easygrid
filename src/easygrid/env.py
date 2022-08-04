"""
This module creates the gym environment wrapped arround the microgrid core
"""

from abc import abstractmethod
from typing import Tuple

import gym
import numpy as np

from easygrid.microgrid import Action, Microgrid

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

    def __init__(self, config: dict) -> None:

        """
        Creates the relevant attributes based on the config

        Args:
            config (dict): Configuration for the underlying microgrid.
        """
        super().__init__()
        self.microgrid = Microgrid(config)
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # # Example for using image as input:
        # self.observation_space = spaces.Box(
        # )

    def step(self, action: Action) -> Tuple[np.ndarray, float, bool, str]:
        """
        Executes the action given by the agent (or something else) and \
        returns information about the state of the environment and reward

        Args:
            action (Action): The action to be processed by the environment,\
                 it should contain:
                - How much to store/discharge in the battery (float)
                - How much to sell/buy from the grid (float)

        Returns:
            Tuple[np.ndarray, float, bool, NoneType]: The observation, reward,\
                done and info following gym template
        """
        observation, done = self.microgrid.run_timestep(action)
        reward = self.compute_reward()
        info = ""
        return observation, reward, done, info

    def reset(self, *args, **kwargs):
        """
        Resets the environment to an initial state and returns this state.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError
        # return observation  # reward, done, info can't be included

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
    def compute_reward(mg: Microgrid) -> float:
        """
        Computes the reward/cost based on the current state of the system.

        Args:
            mg (Microgrid): The microgrid for which we want to compute the \
                cost, the cost will depend of its current state.

        Returns:
            float: The reward/cost
        """
        reward = None
        return reward
