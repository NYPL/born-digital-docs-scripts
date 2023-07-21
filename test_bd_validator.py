import bd_validator as bv
import pytest
from pathlib import Path

@pytest.fixture
def good_package():
    return Path("fixtures/simple_video_pk")

def test_is_package_bag(good_package):
    result = bv.is_valid_bag(good_package)
    assert result is True
