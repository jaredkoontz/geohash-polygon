from geohash_poly.coordinates import Coordinates
from geohash_poly.geohash import GeoHash


class GeoHashUtils:
    @staticmethod
    def decode_with_error(hash_string: str) -> Coordinates:
        bbox = GeoHash.decode_bbox(hash_string)
        lat = (bbox[0] + bbox[2]) / 2
        lon = (bbox[1] + bbox[3]) / 2
        lat_err = bbox[2] - lat
        lon_err = bbox[3] - lon
        return Coordinates(lat, lon, lat_err, lon_err)

    @staticmethod
    def is_west(lon1: float, lon2: float) -> bool:
        return (lon1 < lon2 and lon2 - lon1 < 180) or (
                lon1 > lon2 and lon2 - lon1 + 360 < 180
        )

    @staticmethod
    def poly_to_bb(polygon: list[Coordinates]) -> tuple[float, float, float, float]:
        min_lat = float("inf")
        min_lon = float("inf")
        max_lat = float("-inf")
        max_lon = float("-inf")

        for point in polygon:
            lat = point.get_latitude()
            lon = point.get_longitude()
            min_lat = min(min_lat, lat)
            min_lon = min(min_lon, lon)
            max_lat = max(max_lat, lat)
            max_lon = max(max_lon, lon)

        return min_lat, min_lon, max_lat, max_lon

    @staticmethod
    def neighbor(hash_string: str, direction: tuple[int, int]) -> str:
        coords = GeoHashUtils.decode_with_error(hash_string)
        error = coords.get_error()
        lat_error = error.lat_err if error else 0
        lon_error = error.lon_err if error else 0
        neighbor_lat = coords.get_latitude() + direction[0] * lat_error * 2
        neighbor_lon = coords.get_longitude() + direction[1] * lon_error * 2
        return GeoHash.encode_lat_lon(neighbor_lat, neighbor_lon, len(hash_string))

    @staticmethod
    def inside(point: Coordinates, polygon: list[Coordinates]) -> int:
        if PointInPolygon.point_in_polygon(
                [point.get_longitude(), point.get_latitude()], polygon
        ):
            return 1
        return 0


class PointInPolygon:
    @staticmethod
    def point_in_polygon(point: list[float], polygon: list[Coordinates]) -> bool:
        """
        Ray-casting algorithm to check if point is inside polygon.
        `point` is [lon, lat]; `polygon` is list of Coordinates.
        """
        x, y = point
        num = len(polygon)
        inside = False

        p1x = polygon[0].get_longitude()
        p1y = polygon[0].get_latitude()

        for i in range(num + 1):
            p2x = polygon[i % num].get_longitude()
            p2y = polygon[i % num].get_latitude()
            if min(p1y, p2y) < y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    xinters = float("inf")
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
            p1x, p1y = p2x, p2y

        return inside
