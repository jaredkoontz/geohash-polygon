from geohash_poly.coordinates import Coordinates
from geohash_poly.geohash import GeoHash


def longest_enclosing_hash(
        polygon_points: list[Coordinates], precision: int = GeoHash.DEFAULT_PRECISION
) -> str:
    hashes = [GeoHash.encode(coord, precision) for coord in polygon_points]
    return _longest_common_prefix(hashes)


def _longest_common_prefix(strings: list[str]) -> str:
    if not strings:
        return ""

    # Use the first string as a reference
    for prefix_len in range(len(strings[0])):
        current_char = strings[0][prefix_len]
        for s in strings[1:]:
            if prefix_len >= len(s) or s[prefix_len] != current_char:
                return strings[0][:prefix_len]
    return strings[0]
