import numpy as np
from nav_helpers import to_ecef


def test_to_ecef():
    assert np.allclose(to_ecef(0.0, 0.0, 0.0), [6378137.0, 0.0, 0.0], atol=1e-3)
    assert np.allclose(to_ecef(0.0, 90.0, 0.0), [0.0, 6378137.0, 0.0], atol=1e-3)
