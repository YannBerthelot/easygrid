"""
Example of operating the microgrid using gym environment
"""
from easygrid.config.pymgrid_config import mg_config
from easygrid.env import GridEnv


def main():
    """
    Example of microgrid operation
    """
    env = GridEnv(mg_config)
    done = False
    while not done:
        _, _, done, _ = env.step(env.action_space.sample())
    env.microgrid.show_logs()


if __name__ == "__main__":
    main()
