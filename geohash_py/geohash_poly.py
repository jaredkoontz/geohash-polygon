from shapely.geometry import box
from shapely.geometry import Polygon
from shapely.prepared import prep

from . import geohash


def get_geohash_bbox(geohash_code):
    lat, lon, lat_err, lon_err = geohash.decode_exactly(geohash_code)
    return box(lon - lon_err, lat - lat_err, lon + lon_err, lat + lat_err)


def geohashes_in_polygon(polygon_coords, precision=5):
    polygon = Polygon(polygon_coords)
    prepared_poly = prep(polygon)
    min_lon, min_lat, max_lon, max_lat = polygon.bounds

    # Starting geohash
    min_hash = geohash.encode(min_lat, min_lon, precision)
    max_hash = geohash.encode(max_lat, max_lon, precision)

    # Generate grid of geohashes covering the bounding box
    # Start with bottom-left corner
    lat_step = 0.1  # approximate step, refine based on precision
    lon_step = 0.1

    result = set()
    lat = min_lat
    while lat <= max_lat:
        lon = min_lon
        while lon <= max_lon:
            current_hash = geohash.encode(lat, lon, precision)
            if current_hash not in result:
                gh_box = get_geohash_bbox(current_hash)
                if prepared_poly.intersects(gh_box):
                    result.add(current_hash)
            lon += lon_step
        lat += lat_step

    return result
