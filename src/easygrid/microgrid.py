"""
This module creates thhe microgrid object
"""

from typing import List, Tuple, Union

import numpy as np

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

    def __init__(self, config: dict) -> None:
        """
        Creates the relevant attributes based on the config

        Args:
            config (dict): Configuration for the underlying microgrid.
        """
        battery_config: BatteryConfig = config["BATTERY"]
        grid_config: GridConfig = config["GRID"]
        pv_config: PvConfig = config["PV"]

        self.battery = Battery(battery_config)
        self.grid = Grid(grid_config)
        self.pv = Photovoltaic(pv_config)

        self.t = 0
        self.MAX_TIMESTEP = config["MICROGRID"]["MAX_TIMESTEP"]

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
        # self.load = Load()

    def run_timestep(self, action: Action) -> Tuple[np.ndarray, bool]:
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
        self.battery.charge_discharge(action["battery"])
        self.t += 1
        return self.obs, self.done

    @property
    def obs(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: The current state of the microgrid
        """
        return np.array([self.battery.state_of_charge])

    @property
    def done(self) -> bool:
        """
        Returns:
            bool: Wether or not the microgrid is in a final state
        """
        return self.t >= self.MAX_TIMESTEP

    def print_info(self):
        """
        TBD

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def reset(self):
        """
        TBD

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError


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

    @property
    def state_of_charge(self) -> float:
        """
        Returns:
            float: the current state of charge of the battery (between 0 and 1)
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
        if len(self.import_prices) != len(self.export_prices):
            raise ValueError(
                f"Price timeseries are not of the same length \
                    \n import : {len(self.import_prices)} \
                    \n export : {len(self.export_prices)} "
            )

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

    @property
    def pv_production_ts(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            Union[List[float], np.ndarray]: The production timeserie rescaled.
        """
        return self.pv_production_ts_ * self.production_factor

    @property
    def __len__(self) -> int:
        """
        Returns:
            int: The length of pv production serie for safety checks
        """
        return len(self.pv_production_ts)

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

    @property
    def load_ts(self) -> Union[List[float], np.ndarray]:
        """
        Returns:
            Union[List[float], np.ndarray]: The load timeserie rescaled.
        """
        return self.load_ts_ * self.load_factor

    @property
    def __len__(self) -> int:
        """
        Returns:
            int: The length of pv production serie for safety checks
        """
        return len(self.load_ts)

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
