"""
This module creates thhe microgrid object
"""

from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from easygrid.data.data_utils import DATA_FOLDER, get_indexes
from easygrid.types import Action, BatteryConfig, GridConfig, LoadConfig, PvConfig


class Microgrid:
    """
    This class represents a microgrid and its components
        - Battery
        - Grid
        - PV
        - Load
    It holds the state of the microgrid and how to alter it.
    ...

    Methods
    -------
    run_timestep : executes the action given by the agent (or something else) \
        and returns information about the state of the environmen
    print_info : TBD
    reset : resets the environment to an initial state and returns this state.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, config: dict) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            config (dict): Configuration for the underlying microgrid.
        """
        battery_config: BatteryConfig = config["BATTERY"]
        grid_config: GridConfig = config["GRID"]
        pv_config: PvConfig = config["PV"]
        load_config: LoadConfig = config["LOAD"]
        self.indexes = get_indexes(data_folder=DATA_FOLDER)

        self.battery = Battery(battery_config)
        self.grid = Grid(grid_config)
        self.pv = Photovoltaic(pv_config)
        self.load = Load(load_config)

        mg_config = config["MICROGRID"]  # flor clarity purposes
        self.overproduction_penalty = mg_config["overprod_penalty"]
        self.underproduction_penalty = mg_config["underprod_penalty"]
        self.MAX_TIMESTEP = mg_config["max_timestep"]

        self.t = 0
        self.delta_t = 1

        self._init_logs_()

        if self.grid.__len__ < self.MAX_TIMESTEP:
            raise ValueError(
                f"Prices timeseries are shorter ({self.grid.__len__ }) than \
                    the maximum number of timesteps ({self.MAX_TIMESTEP})"
            )
        if self.pv.__len__ < self.MAX_TIMESTEP:
            raise ValueError(
                f"PV production timeseries are shorter ({self.pv.__len__ }) \
                    than the maximum number of timesteps ({self.MAX_TIMESTEP})"
            )

    @property
    def config(self) -> dict:
        """
        Returns:
            dict: The current microgrid config
        """
        return {
            "battery": self.battery.config,
            "grid": self.grid.config,
            "load": self.load.config,
            "pv": self.pv.config,
            "microgrid": {
                "overprod_penalty": self.overproduction_penalty,
                "underprod_penalty": self.underproduction_penalty,
                "max_timestep": self.MAX_TIMESTEP,
            },
        }

    @property
    def __len__(self):
        return min(self.load.__len__, self.pv.__len__, self.grid.__len__)

    def run_timestep(
        self, action: Action, logging: bool = True
    ) -> Tuple[np.ndarray, bool]:
        """
        Executes the action on the microgrid and computes the following state

        Args:
            action (Action): The action to be processed by the environment,\
                 it should contain:
                - How much to store/discharge in the battery (float)
                - How much to sell/buy from the grid (float)

        Returns:
            Tuple[np.ndarray, bool]: The next state and terminal state flag
        """
        self.t += 1

        energy_battery = action["battery"]
        energy_grid = action["grid"]
        energy_pv = self.pv.get_power(self.t) * self.delta_t
        energy_load = self.load.get_load(self.t) * self.delta_t
        energy_balance = energy_pv + energy_grid - energy_load - energy_battery

        overcharge = self.battery.charge_discharge(energy_battery)
        overcharge_cost = self.battery.get_overcharge_cost(overcharge)
        grid_cost = self.grid.get_cost(self.t, energy_grid)
        error_cost = self.get_error_cost(energy_balance)

        if logging:
            self.log_energies(
                energy_battery, energy_grid, energy_pv, energy_load, energy_balance
            )
            self.log_costs(overcharge_cost, grid_cost, error_cost)
        return self.obs, self.done

    def get_error_cost(self, energy_balance: float) -> float:
        """
        Compute the cost for not prodiving the right amount of energy.
        Either too much or not enough

        Args:
            energy (float): the energy balance (overprod:+, underprod:-)

        Returns:
            float: The cost ($) for not meeting the requirement
        """
        if energy_balance >= 0:
            return energy_balance * self.overproduction_penalty
        else:
            return energy_balance * self.underproduction_penalty

    def _init_logs_(self):
        """
        Initialize lists for logging energies and costs.
        """
        self.energies = {"balance": [], "battery": [], "grid": [], "pv": [], "load": []}
        self.costs = {"total": [], "overcharge": [], "grid": [], "error": []}

    def log_energies(
        self, battery: float, grid: float, pv: float, load: float, balance: float = None
    ):
        """
        Log the different energies collected at the current timestep

        Args:
            battery (float): The energy charged in or withdrawn from the battery
            grid (float): The energy bought (+) or sold (-) to the grid
            pv (float): The energy produced from the pv panels
            load (float): The energy required by the local network
            balance (float, optional): The energy balance. Defaults to None.
        """
        # pylint: disable=too-many-arguments

        if balance is None:
            balance = pv + grid - load - battery
        self.energies["battery"].append(battery)
        self.energies["grid"].append(grid)
        self.energies["pv"].append(pv)
        self.energies["load"].append(load)
        self.energies["balance"].append(balance)

    def log_costs(self, overcharge: float, grid: float, error: float):
        """
        Log the different costs collected at the current timestep

        Args:
            overcharge (float): The costs due to overcharging or undercharging \
                the battery
            grid (float): The costs of operating the grid (buying:+ or selling:-)
            error (float): The costs due to not meeting the local energy requirements
        """
        self.costs["overcharge"].append(overcharge)
        self.costs["grid"].append(grid)
        self.costs["error"].append(error)
        self.costs["total"].append(overcharge + grid + error)

    def get_logs(self) -> dict:
        """
        Return the logs in a dict format for energies and costs

        Returns:
            dict: Costs and energies logs.
        """
        return {"costs": self.costs, "energies": self.energies}

    def show_logs(self, show=True) -> Union[None, Tuple[plt.Axes]]:
        """
        Plot the available logs in a simple fashion.

        Args:
            show (bool, optional): Wether or not to show the graphs or return \
                the matplotlib figs instead for later use. Defaults to True.

        Returns:
            Any[None, Tuple[plt.Axes]]: Either nothing or the created figures.
        """
        figures = []
        for data_name, data in self.get_logs().items():
            fig, ax = plt.subplots(len(data), 1, figsize=(8, 6))
            for i, (name, points) in enumerate(data.items()):
                ax[i].plot(points)
                ax[i].set_title(name.capitalize())
            plt.suptitle(data_name.capitalize())
            plt.tight_layout()
            if show:
                plt.show()
            else:
                figures.append(fig)
        if not show:
            return figures

    @property
    def obs(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: The current state of the microgrid
        """
        return np.array(
            [
                self.battery.state_of_charge,
                self.grid.import_prices[self.t + 1],
                self.grid.export_prices[self.t + 1],
                self.load.get_load(self.t + 1),
                self.pv.get_power(self.t + 1),
            ]
        )

    @property
    def done(self) -> bool:
        """
        Returns:
            bool: Wether or not the microgrid is in a final state
        """
        return (
            self.t >= self.MAX_TIMESTEP - 1
        )  # to allow to see the upcoming prices and load before taking action

    def print_info(self):
        """
        TBD

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def reset(self, reset_logs=False) -> np.ndarray:
        """
        Reset the microgrid in its original state.

        Args:
            reset_logs (bool, optional): Wether or not to reset the log arrays.\
                Defaults to False.

        Returns:
            np.ndarray: The initial observation of the environment
        """
        self.t = 0
        self.battery.reset()
        if reset_logs:
            self._init_logs_()
        return self.obs

    def set_battery_from_duration(self, nb_of_hours: float) -> None:
        """
        Set the battery config to handle a given number of hours under mean load

        Args:
            nb_of_hours (float): The capacity of the battery in hours
        """
        self.battery.capacity = self.load.__mean__ * nb_of_hours
        self.battery.max_output = max(self.battery.max_output, self.load.__mean__)

    # def set_pv_from_load(self, nb_of_hours: float) -> None:
    #     """
    #     Set the pv production capacity to a faction of the yearly load it can handle
    #     Args:
    #         nb_of_hours (float): The capacity of the battery in hours
    #     """
    #     self.battery.capacity = self.load.__mean__ * nb_of_hours


class Battery:
    """
    Models the battery, its state and relevant actions
    ...

    Attributes
    ----------
    capacity : float
        The total capacity of the battery.
    high_capacity : float
        The higher energy threshold to be stored in the battery \
            for maximum efficiency of the battery
    low_capacity : float
        The lower energy threshold to be stored in the battery \
            for maximum efficiency of the battery
    max_output : float
        The maximum power output of the battery (which defines the maximal\
             amount of energy that can be transfered in a single timestep)
    min_output : float
        The minimum power output of the battery (which defines the minimal\
             amount of energy that can be transfered in a single timestep)
    _energy : float
        The current amount of energy stored in the battery. Private.
    state_of_charge (property) : float
        The state of charge of the battery (between 0 and 1)
    energy (property) : float
        The current amount of energy stored in the battery. Includes safety \
            check for negative energy

    Methods
    -------
    charge_discharge : Stores or discharge the required amount of energy \
        into/from the battery and computes the under/overcharge
    """

    def __init__(self, battery_config: BatteryConfig) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            battery_config (BatteryConfig): Configuration for the battery.
        """
        self.capacity = battery_config["capacity"]
        self.high_capacity = battery_config["high_capacity"]
        self.low_capacity = battery_config["low_capacity"]
        self.max_output = battery_config["max_output"]
        self.min_output = battery_config["min_output"]
        self._energy = battery_config["initial_energy"]
        self.initial_energy = battery_config["initial_energy"]
        self.overcharge_penalty = battery_config["overcharge_penalty"]

    def reset(self):
        """
        Reset the battery energy/soc to the initial setting
        """
        self._energy = self.initial_energy

    @property
    def config(self) -> dict:
        """

        Returns:
            dict: The current battery config
        """
        return {
            "capacity": self.capacity,
            "high_capacity": self.high_capacity,
            "low_capacity": self.low_capacity,
            "max_output": self.max_output,
            "min_output": self.min_output,
            "overcharge_penalty": self.overcharge_penalty,
            "initial_energy": self.initial_energy,
        }

    @property
    def state_of_charge(self) -> float:
        """
        Returns:
            float: the current state of charge of the battery \
                (between 0 : empty and 1 : full)
        """
        soc = self._energy / self.capacity
        assert (
            0 <= soc <= 1
        ), f"Soc not between 0 and 1 : {soc} ({self._energy}/{self.capacity})"
        return soc

    @property
    def energy(self) -> float:
        """
        Returns:
            float: The current energy quantity stored in the battery
        """
        if self._energy >= 0:
            return self._energy
        else:
            raise ValueError(f"Energy is negative ({self._energy}), there is a problem")

    def charge_discharge(self, energy: float) -> float:
        """
        Charge/Discharge the battery with the desired quantity of energy

        Args:
            energy (float): The energy to be stored (+)/discharged (-)

        Returns:
            float: The excess/missing energy when compared to max and min \
                thresholds
        """
        new_energy = self.energy + energy
        if energy >= 0:
            # if there is more energy than the upper bound, we compute \
            # the excess
            overcharge = min(0, new_energy - self.high_capacity)
            self._energy = min(self.high_capacity, new_energy)
            return overcharge
        else:
            # if there is less energy than the lower bound, we compute \
            # how much is missing
            undercharge = max(0, self.low_capacity - new_energy)
            self._energy = max(self.low_capacity, new_energy)
            return undercharge

    def get_overcharge_cost(self, overcharge: float) -> float:
        """
        Compute the overcharge cost for not meeting the optimal battery thresholds

        Args:
            overcharge (float): The quantity of energy outside the correct range.

        Returns:
            float: The corresponding cost for underoptimal operation of the battery
        """
        return overcharge * self.overcharge_penalty


class Grid:
    """
    Models the grid, its costs and prices
    ...

    Attributes
    ----------
    import_prices : List[float]
        The timeserie for import prices (one price per timestep)
    export_prices : List[float]
        The timeserie for export prices (one price per timestep)
    import_prices_factor : float
        A scaling factor to easily modify the import prices.
    export_prices_factor : float
        A scaling factor to easily modify the export prices.
    __len__ (property) : int
        The length of timeseries for safety checks

    Methods
    -------
    get_cost : Get the running cost for a given timestep and energy to be \
        bought/sold
    """

    def __init__(self, grid_config: GridConfig) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            grid_config (GridConfig): Configuration for the grid.
        """
        self.import_prices_ = grid_config["import_prices"]
        self.export_prices_ = grid_config["export_prices"]
        self.import_price_factor = 1
        self.export_price_factor = 1
        if "import_price_factor" in grid_config.keys():
            self.import_price_factor = grid_config["import_price_factor"]
        if "export_price_factor" in grid_config.keys():
            self.export_price_factor = grid_config["export_price_factor"]

        if len(self.import_prices) != len(self.export_prices):
            raise ValueError(
                f"Price timeseries are not of the same length \
                    \n import : {len(self.import_prices)} \
                    \n export : {len(self.export_prices)} "
            )

    @property
    def config(self) -> dict:
        """
        Returns:
            dict: The current grid config
        """
        return {
            "import_prices": self.import_prices,
            "export_prices": self.export_prices,
            "import_price_factor": self.import_price_factor,
            "export_price_factor": self.export_price_factor,
        }

    def get_cost(self, t: int, energy: float) -> float:
        """
        Get the cost for operating the grid with the required amount of energy

        Args:
            t (int): The timestep for which the costs must be computed
            energy (float): Energy to be sold (-) or bought (+)

        Returns:
            float: The cost in euros, positive is loss, negative is gain
        """
        if energy >= 0:
            cost = self.import_prices[t] * energy
        else:
            cost = self.export_prices[t] * energy
        return cost

    @property
    def __len__(self) -> int:
        """
        Returns:
            int: The length of prices series for safety checks
        """
        return len(self.import_prices)

    @property
    def import_prices(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            int: The length of prices series for safety checks
        """
        return self.import_prices_ * self.import_price_factor

    @property
    def export_prices(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            int: The length of prices series for safety checks
        """
        return self.export_prices_ * self.export_price_factor


class Photovoltaic:
    """
    Models the photovoltaic local production
    ...

    Attributes
    ----------
    pv_production_ts_ : List[float]
        The timeserie for pv_production prices (power available per timestep).
    production_factor : float
        A scaling factor to easily modify the pv production.
    __len__ (property) : int
        The length of timeseries for safety checks.

    Methods
    -------
    get_cost : Get the power produced by PV for a given timestep.
    """

    def __init__(self, pv_config: PvConfig) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            pv_config (PvConfig): Configuration for the PV.
        """
        self.pv_production_ts_ = pv_config["pv_production_ts"]
        self.production_factor = 1
        if "production_factor" in pv_config.keys():
            self.production_factor = pv_config["production_factor"]

    @property
    def config(self) -> dict:
        """

        Returns:
            dict: The current pv config
        """
        return {
            "pv_production_ts": self.pv_production_ts,
            "production_factor": self.production_factor,
        }

    @property
    def pv_production_ts(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            Union[List[float], np.ndarray]: The production timeserie rescaled.
        """
        return np.array(self.pv_production_ts_) * self.production_factor

    @property
    def __len__(self) -> int:
        """
        Returns:
            int: The length of pv production serie for safety checks
        """
        return len(self.pv_production_ts)

    @property
    def __mean__(self) -> int:
        """
        Returns:
            int: The mean of the pv production accross the timeserie
        """
        return np.mean(self.pv_production_ts)

    def get_power(self, t: int) -> float:
        """
        Method to get the power produced for the given timestep.\
            Not really interesting, it exists for an easier framework.

        Args:
            t (int): the timestep for which to return power

        Returns:
            float: the corresponding produced photovoltaic power.
        """
        return self.pv_production_ts[t]


class Load:
    """
    Models the local consumption of energy
    ...

    Attributes
    ----------
    load_ts_ : List[float]
        The timeserie for load requirements (power required per timestep).
    load_factor : float
        A scaling factor to easily modify the load requirement.
    __len__ (property) : int
        The length of timeseries for safety checks.

    Methods
    -------
    get_load : Get the load required for a given timestep
    """

    def __init__(self, load_config: LoadConfig) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            load_config (LoadConfig): Configuration for the load.
        """
        self.load_ts_ = load_config["load_ts"]
        self.load_factor = 1.0
        if "load_factor" in load_config.keys():
            self.load_factor = load_config["load_factor"]

    @property
    def config(self) -> dict:
        """
        Returns:
            dict: The current load config
        """
        return {
            "load_ts": self.load_ts,
            "load_factor": self.load_factor,
        }

    @property
    def load_ts(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            Union[List[float], np.ndarray]: The load timeserie rescaled.
        """
        return np.array(self.load_ts_) * self.load_factor

    @property
    def __len__(self) -> int:
        """
        Returns:
            int: The length of the load timeserie
        """
        return len(self.load_ts)

    @property
    def __mean__(self) -> int:
        """
        Returns:
            int: The mean of the load accross the timeserie
        """
        return np.mean(self.load_ts)

    def get_load(self, t: int) -> float:
        """
        Method to get the load required for the given timestep.\
            Not really interesting, it exists for an easier framework.

        Args:
            t (int): the timestep for which to return load
        Returns:
            float: the corresponding load required by the local network
        """
        return self.load_ts[t]
