import pytest

from geohash_py import geohashes_in_polygon
from geohash_py import longest_enclosing_hash
from test.test_data import no_co
from test.test_data import PolygonInfo
from test.test_data import us
from test.test_data import weird
from test.test_data import wyoming_co


@pytest.mark.parametrize(
    "poly",
    [
        us,
        wyoming_co,
        no_co,
        weird,
    ],
)
def test_geohashes_in_polygon(poly: PolygonInfo):
    leh = longest_enclosing_hash(poly.coords)
    precision = len(leh) + 2
    hashes = geohashes_in_polygon(poly.coords, precision)
    assert hashes is not None


@pytest.mark.parametrize(
    "poly",
    [
        us,
        wyoming_co,
        no_co,
        weird,
    ],
)
def test_longest_enclosing_hash(poly: PolygonInfo):
    precision = 6
    leh = longest_enclosing_hash(poly.coords, precision)
    assert leh == poly.hash
