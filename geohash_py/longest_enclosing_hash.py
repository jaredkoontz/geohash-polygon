from shapely.geometry.geo import box
from shapely.geometry.polygon import Polygon
from shapely.prepared import prep

from geohash_py import geohash


def longest_enclosing_hash(
    polygon_points: list[tuple[float, float]], precision: int = 12
):
    """
    Given a list of (lat, lon) tuples representing polygon points,
    find the longest common geohash prefix that encloses all points.
    """
    if not polygon_points:
        return ""

    # Encode all points to geohash at max precision
    hashes = [geohash.encode(lat, lon, precision) for lat, lon in polygon_points]

    # Find the longest common prefix
    min_len = min(len(h) for h in hashes)
    prefix = ""

    for i in range(min_len):
        c = hashes[0][i]
        if all(h[i] == c for h in hashes):
            prefix += c
        else:
            break

    return prefix


def get_geohash_bbox(gh):
    lat, lon, lat_err, lon_err = geohash.decode_exactly(gh)
    return box(lon - lon_err, lat - lat_err, lon + lon_err, lat + lat_err)


def longest_enclosing_geohashes(polygon_coords, max_precision=7):
    polygon = Polygon(polygon_coords)
    prepared_poly = prep(polygon)

    min_lon, min_lat, max_lon, max_lat = polygon.bounds
    min_hash = geohash.encode(min_lat, min_lon, 1)
    max_hash = geohash.encode(max_lat, max_lon, 1)

    queue = set()
    visited = set()

    # Start with all possible precision 1 geohashes that intersect bbox
    for lat in range(int(min_lat) - 1, int(max_lat) + 2):
        for lon in range(int(min_lon) - 1, int(max_lon) + 2):
            gh = geohash.encode(lat, lon, 1)
            queue.add(gh)

    result = set()

    while queue:
        gh = queue.pop()
        if gh in visited:
            continue
        visited.add(gh)

        gh_box = get_geohash_bbox(gh)

        if prepared_poly.contains(gh_box):
            # Fully inside, add to result, don’t subdivide
            result.add(gh)
        # elif prepared_poly.intersects(gh_box):
        #     # Partially inside, subdivide if precision < max
        #     if len(gh) < max_precision:
        #         # for c in geohash.expand(gh):
        #         queue.add(c)

    return result
