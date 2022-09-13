"""
Type helpers for the project
"""
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


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

    import_prices: Path
    export_prices: Path
    import_price_factor: Optional[float] = 1.0
    export_price_factor: Optional[float] = 1.0


class PvConfig(BaseModel):
    """
    This TypedDict represents the pv panel config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    pv_production_ts: Path
    production_factor: Optional[float] = 1.0


class LoadConfig(BaseModel):
    """
    This TypedDict represents the load config template to be fed \
        to the microgrid
    """

    # ts for timeserie
    load_ts: Path
    load_factor: Optional[float] = 1.0


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
