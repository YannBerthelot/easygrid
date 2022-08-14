"""
Type helpers for the project
"""
from typing import List, TypedDict, Union

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


class GridConfig(TypedDict):
    """
    This TypedDict represents the grid config template to be fed \
        to the microgrid
    """

    import_prices: Union[List[float], np.ndarray]
    export_prices: Union[List[float], np.ndarray]


class PvConfig(TypedDict):
    """
    This TypedDict represents the pv panel config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    pv_prouction_ts: Union[List[float], np.ndarray]


class LoadConfig(TypedDict):
    """
    This TypedDict represents the load config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    load_ts: Union[List[float], np.ndarray]
