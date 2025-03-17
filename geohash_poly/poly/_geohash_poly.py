from geohash_poly.coordinates import Coordinates
from geohash_poly.geohash import GeoHash
from geohash_poly.geohash import GeoHashUtils


def geohashes_in_polygon(polygon: list[Coordinates], precision: int) -> set[str]:
    return _hashes_in_poly(polygon, precision)


def _hashes_in_poly(polygon: list[Coordinates], precision: int) -> set[str]:
    bounding = GeoHashUtils.poly_to_bb(polygon)
    all_hashes = set()

    row_hash = GeoHash.encode_lat_lon(bounding[2], bounding[1], precision)
    row_box = GeoHash.decode_bbox(row_hash)

    while row_box[2] > bounding[0]:  # While maxLat > minLat of bounding box
        column_hash = row_hash
        column_box = row_box

        while GeoHashUtils.is_west(column_box[1], bounding[3]):
            inside = GeoHashUtils.inside(
                GeoHashUtils.decode_with_error(column_hash), polygon
            )
            if inside % 2 == 1:
                all_hashes.add(column_hash)
            column_hash = GeoHashUtils.neighbor(column_hash, (0, 1))  # Move east
            column_box = GeoHash.decode_bbox(column_hash)

        row_hash = GeoHashUtils.neighbor(row_hash, (-1, 0))  # Move south
        row_box = GeoHash.decode_bbox(row_hash)

    return all_hashes
