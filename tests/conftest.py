import os

import pytest


@pytest.fixture()
def test_data_dir():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dir, "data")
