import gym

from easygrid.microgrid import Microgrid

# from gym import spaces


class GridEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human"]}

    def __init__(self, config):
        super().__init__()
        self.microgrid = Microgrid(config)
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # # Example for using image as input:
        # self.observation_space = spaces.Box(
        # )

    def step(self, action):
        self.microgrid.run_timestep(action)
        # return observation, reward, done, info

    def reset(self, *args, **kwargs):
        raise NotImplementedError
        # return observation  # reward, done, info can't be included

    def render(self, mode="human"):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
