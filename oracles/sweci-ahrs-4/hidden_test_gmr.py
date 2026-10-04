import numpy as np
from nav_helpers import row_distances


def test_row_distances():
    A = np.array([[0.0, 0.0, 0.0], [1.0, 2.0, 2.0]])
    B = np.array([[3.0, 4.0, 0.0], [1.0, 2.0, 2.0]])
    assert np.allclose(row_distances(A, B), [5.0, 0.0])
