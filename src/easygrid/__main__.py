"""
Example of operating the microgrid
"""
import numpy as np

from easygrid.config.pymgrid_config import config
from easygrid.microgrid import Microgrid
from easygrid.types import Action


def main():
    """
    Example of microgrid operation
    """
    mg = Microgrid(config)
    for _ in range(mg.__len__ - 1):
        action: Action = {
            "battery": 0,
            "grid": np.random.randint(1e3),
        }
        mg.run_timestep(action)
    mg.show_logs()


if __name__ == "__main__":
    main()
