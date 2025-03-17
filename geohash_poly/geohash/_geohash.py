from geohash_poly.coordinates.coordinates import Coordinates


class GeoHash:
    BITS_PER_CHAR = 5
    LATITUDE_RANGE = 90.0
    LONGITUDE_RANGE = 180.0
    DEFAULT_PRECISION = 12

    # GeoHash base32 character map
    char_map = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "j",
        "k",
        "m",
        "n",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    # Reverse map for decoding
    char_lookup_table = {c: i for i, c in enumerate(char_map)}

    @staticmethod
    def encode(coordinates: Coordinates, precision: int = DEFAULT_PRECISION) -> str:
        return GeoHash.encode_lat_lon(
            coordinates.lat_lon_pair.lat,
            coordinates.lat_lon_pair.lon,
            precision,
        )

    @staticmethod
    def encode_lat_lon(latitude: float, longitude: float, precision: int) -> str:
        high = [GeoHash.LONGITUDE_RANGE, GeoHash.LATITUDE_RANGE]
        low = [-GeoHash.LONGITUDE_RANGE, -GeoHash.LATITUDE_RANGE]
        value = [longitude, latitude]

        hash_string = ""

        for p in range(precision):
            char_bits = 0
            for b in range(GeoHash.BITS_PER_CHAR):
                bit = p * GeoHash.BITS_PER_CHAR + b
                idx = bit % 2
                middle = (high[idx] + low[idx]) / 2
                char_bits <<= 1

                if value[idx] > middle:
                    char_bits |= 1
                    low[idx] = middle
                else:
                    high[idx] = middle

            hash_string += GeoHash.char_map[char_bits]

        return hash_string

    @staticmethod
    def decode_bbox(hash_string: str) -> tuple[float, float, float, float]:
        hash_string = hash_string.lower()
        is_lon = True
        max_lat, min_lat = 90.0, -90.0
        max_lon, min_lon = 180.0, -180.0

        for char in hash_string:
            hash_value = GeoHash.char_lookup_table[char]

            for bits in range(4, -1, -1):
                bit = (hash_value >> bits) & 1
                if is_lon:
                    mid = (max_lon + min_lon) / 2
                    if bit == 1:
                        min_lon = mid
                    else:
                        max_lon = mid
                else:
                    mid = (max_lat + min_lat) / 2
                    if bit == 1:
                        min_lat = mid
                    else:
                        max_lat = mid
                is_lon = not is_lon

        return min_lat, min_lon, max_lat, max_lon
