from unittest.mock import patch

import matplotlib.pyplot as plt

from easygrid.math_utils import get_hourly_variation


@patch("matplotlib.pyplot.show")
def test_hourly_variation(mock_show):
    gen = get_hourly_variation(
        max_val=10, min_val=3, period=24, time_max=15, time_min=3, size=100
    )
    points = [i for i in gen]
    plt.plot(points)
    plt.show()
