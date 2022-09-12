"""
Example of operating the microgrid
"""
import numpy as np

from easygrid.config.pymgrid_config import mg_config
from easygrid.microgrid import Microgrid
from easygrid.types import Action


def main():
    """
    Example of microgrid operation
    """
    mg = Microgrid(mg_config)
    for _ in range(mg.__len__ - 2):
        action = Action.parse_obj(
            {
                "battery": 0,
                "grid": np.random.randint(1e3),
            }
        )
        mg.run_timestep(action)
    mg.show_logs()


if __name__ == "__main__":
    main()
