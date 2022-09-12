import pytest
from pydantic.error_wrappers import ValidationError

from easygrid.types import PvConfig


def test_NDArray():
    with pytest.raises(ValidationError):
        PvConfig.parse_obj(
            {
                "pv_production_ts": [12, 3],
            }
        )
