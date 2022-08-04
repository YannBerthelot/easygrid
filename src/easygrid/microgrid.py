"""
This module creates thhe microgrid object
"""

from typing import Tuple, TypedDict

import numpy as np


class Action(TypedDict):
    """
    This TypedDict represents the action template to be fed to the microgrid
    """

    battery: float
    grid: float


class BatteryConfig(TypedDict):
    """
    This TypedDict represents the battery config template to be fed \
        to the microgrid
    """

    capacity: float
    high_capacity: float
    low_capacity: float
    max_output: float
    min_output: float
    initial_energy: float


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
        self.battery = Battery(battery_config)
        self.t = 0
        self.MAX_TIMESTEP = config["MICROGRID"]["MAX_TIMESTEP"]
        # self.grid = Grid()
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
            battery_config (dict): Configuration for the battery.
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
        assert self._energy >= 0, "Energy is negative, there is a problem"
        if self._energy >= 0:
            return self._energy

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


# class Grid:
#     def __init__(self) -> None:
#         pass


# class Load:
#     def __init__(self) -> None:
#         pass
