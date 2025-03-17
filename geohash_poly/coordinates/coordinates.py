class LatLonPair:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def get_lat(self) -> float:
        return self.lat

    def get_lon(self) -> float:
        return self.lon

    def __str__(self):
        return f"LatLonPair(lat={self.lat}, lon={self.lon})"


class Error:
    def __init__(self, lat_err: float, lon_err: float):
        self.lat_err = lat_err
        self.lon_err = lon_err

    def __str__(self):
        return f"Error(lat_err={self.lat_err}, lon_err={self.lon_err})"


class Coordinates:
    def __init__(
        self, lat: float, lon: float, lat_err: float = None, lon_err: float = None
    ):
        self.lat_lon_pair = LatLonPair(lat, lon)
        self.error = (
            Error(lat_err, lon_err)
            if lat_err is not None and lon_err is not None
            else None
        )

    def get_latitude(self) -> float:
        return self.lat_lon_pair.get_lat()

    def get_longitude(self) -> float:
        return self.lat_lon_pair.get_lon()

    def get_error(self):
        return self.error

    def __str__(self):
        return f"{self.lat_lon_pair} | {self.error}"
