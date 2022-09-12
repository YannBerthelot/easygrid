"""
Example of operating the microgrid
"""
from easygrid.config.pymgrid_config import mg_config
from easygrid.env import GridEnv


def main():
    """
    Example of microgrid operation
    """
    env = GridEnv(mg_config)
    done = False
    i = 0
    while not done:
        print(i)
        _, _, done, _ = env.step(env.action_space.sample())
        i += 1
    env.microgrid.show_logs()


if __name__ == "__main__":
    main()
