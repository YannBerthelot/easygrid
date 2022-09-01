"""
Math utilitary functions
"""
from math import pi, sin


def get_hourly_variation(
    max_val: float,
    min_val: float,
    period: float,
    time_max: float,
    time_min: float,
    size: int,
) -> list:
    """
    # Build a sin function out of the desired parameters to model an hourly \
    # variation of a variable.

    Args:
        max_val (float): maximal amplitude of the variations
        min_val (float): minimal amplitude of the variations
        period (float): period of the signal
        time_max (float): what time in the period should the max value happen
        time_min (float): what time in the period should the min value happen
        size (int): how much hours should be generated

    Returns:
        list: _description_

    Yields:
        Iterator[list]: The hourly variations of the desired form.
    """
    A = 0.5 * (max_val - min_val)
    d = 0.5 * (time_max + time_min)
    c = 0.5 * (max_val + min_val)
    for i in range(size):
        B = 2 * pi / period
        yield A * sin(B * (i - d)) + c
