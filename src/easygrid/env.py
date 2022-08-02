import gym
from gym import spaces

from easygrid.microgrid import Microgrid


class GridEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human"]}

    def __init__(self, arg1, arg2):
        super(GridEnv, self).__init__()
        self.microgrid = Microgrid()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input:
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8
        )

    def step(self, action):
        self.microgrid.run_timestep(action)
        raise NotImplementedError
        # return observation, reward, done, info

    def reset(self):
        raise NotImplementedError
        # return observation  # reward, done, info can't be included

    def render(self, mode="human"):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
