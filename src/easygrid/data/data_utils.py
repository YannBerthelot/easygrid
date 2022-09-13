"""
External data handling helpers
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

DATA_FOLDER = os.path.dirname(__file__)


def load_data(path: Path) -> np.ndarray:
    """
    Read the data based on the file path

    Args:
        file (path to the correct file): _description_

    Raises:
        ValueError: _description_

    Returns:
        list: _description_
    """
    if not str(path).endswith(".csv"):
        raise ValueError(f"The given path to file is not a csv file : {path}")
    data = pd.read_csv(path)
    assert len(data.columns) == 1
    return np.array(data.values.flatten())


def get_indexes(data_folder) -> dict:
    """
    Get the indexes for all data folders that allow the user to see what data \
    is available

    Args:
        data_folder (str): the folder where the package data is stored

    Returns:
        dict: A dict with the different data types (pv, load, co2) as keys \
            and available data in list as values
    """
    dirs = [
        os.path.join(data_folder, d)
        for d in os.listdir(data_folder)
        if os.path.isdir(os.path.join(data_folder, d))
    ]
    indexes = {}
    for directory in dirs:
        indexes[directory.split("/")[-1]] = get_index(directory)
    return indexes


def get_index(data_folder) -> list:
    """
    Create the index that lists the different files available
    Returns:
        list: _description_
    """
    return [
        os.path.join(data_folder, f)
        for f in os.listdir(data_folder)
        if f.endswith(".csv")
    ]
