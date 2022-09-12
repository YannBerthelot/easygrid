"""
Type helpers for the project
"""
from typing import Any, Optional

import numpy as np
from pydantic import BaseModel

JSON_ENCODERS = {np.ndarray: lambda arr: arr.tolist()}


class NumpyNDArray(np.ndarray):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> np.ndarray:
        # validate data...
        if not isinstance(v, np.ndarray):
            raise TypeError(f"numpy.ndarray required (currently {type(v)})")
        return v


# class Action(BaseModel):
#     """
#     This TypedDict represents the action template to be fed to the microgrid
#     """

#     battery: float
#     grid: float


class BatteryConfig(BaseModel):
    """
    This TypedDict represents the battery config template to be fed \
        to the microgrid
    """

    capacity: float
    high_capacity: float
    low_capacity: float
    max_output: float
    min_output: float
    initial_energy: Optional[float] = 0
    overcharge_penalty: float


class GridConfig(BaseModel):
    """
    This TypedDict represents the grid config template to be fed \
        to the microgrid
    """

    import_prices: NumpyNDArray
    export_prices: NumpyNDArray
    import_price_factor: Optional[float] = 1.0
    export_price_factor: Optional[float] = 1.0

    class Config:
        json_encoders = JSON_ENCODERS


class PvConfig(BaseModel):
    """
    This TypedDict represents the pv panel config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    pv_production_ts: NumpyNDArray
    production_factor: Optional[float] = 1.0

    class Config:
        json_encoders = JSON_ENCODERS


class LoadConfig(BaseModel):
    """
    This TypedDict represents the load config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    load_ts: NumpyNDArray
    load_factor: Optional[float] = 1.0

    class Config:
        json_encoders = JSON_ENCODERS


class MicrogridConfig(BaseModel):
    """
    This TypedDict represents the battery config template to be fed \
        to the microgrid
    """

    max_timestep: int
    overprod_penalty: float
    underprod_penalty: float
    pv: PvConfig
    load: LoadConfig
    grid: GridConfig
    battery: BatteryConfig

    class Config:
        json_encoders = JSON_ENCODERS


# def check_type(param: Any, param_name: str, types: tuple):
#     """
#     Assess right type for a given param or raise ValueError \
#         with explicit explanation

#     Args:
#         param (Any): The value to check
#         param_name (str): The name to associate to the value
#         types (tuple): The acceptable types

#     Raises:
#         ValueError: Explanation of why the check failed
#     """
#     if not isinstance(param, types):
#         raise ValueError(
#             f"Parameter {param_name} ({param}) is \
#                         not of float or int type, but \
#                             {type(param)} type"
#         )
