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
