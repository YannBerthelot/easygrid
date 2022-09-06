import os

import pytest

from easygrid.data.data_utils import DATA_FOLDER, get_indexes, load_data


def test_data_utils():
    with pytest.raises(ValueError):
        load_data(os.path.join(os.getcwd(), "config.py"))
    INDEXES = get_indexes(DATA_FOLDER)
    assert ("pv" in INDEXES.keys()) and ("load" in INDEXES.keys())
    assert len(load_data(INDEXES["pv"][0])) > 0
