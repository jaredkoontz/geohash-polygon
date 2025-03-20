# geohash-polygon-py

A python implementation to find the geohashes inside a polygon. This project is
inspired [from](https://github.com/derrickpelletier/geohash-poly) and
my [java implementation](https://github.com/jaredkoontz/GeoHashesInPolygon/). The java version is used in
my [GeoLens Project](http://www.cs.colostate.edu/geolens) to decide the
resolution of GeoHash tiles to display.

This method is called the longest enclosing hash. In this algorithm, we find the smallest geohash tile that would fully
enclose the geohash. More information about this can be found in
our [publications](http://www.cs.colostate.edu/geolens/entry/publications/publications.php)

This package can find geohashes inside a polygon and can return a polygon given by geohashes.

## Requirements

There are no external dependencies, all that is required is python.

- Python >= 3.x.

## Installation

### Dev

#### Install uv

https://docs.astral.sh/uv/getting-started/installation/

#### Syncing and Testing

```shell
# install
uv sync --all-extras --dev
# run tests
uv run python -m pytest .
```

### User

If there is interest I will host this on pypi.

## Usage

Here is a simple example:

```python
# get geohashes from a polygon
from geohash_poly.coordinates import Coordinates
from geohash_poly.leh import longest_enclosing_hash
from geohash_poly.poly import geohashes_in_polygon

wyoming_co = [
    Coordinates(44.99588261816546, -109.248046875),
    Coordinates(38.238180119798635, -109.1162109375),
    Coordinates(38.41055825094609, -102.8320312),
]
leh = longest_enclosing_hash(wyoming_co)
precision = len(leh) + 2
hashes = geohashes_in_polygon(wyoming_co, precision)
assert len(hashes) == 15
```
