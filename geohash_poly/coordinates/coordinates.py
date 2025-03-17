import dataclasses


@dataclasses.dataclass
class LatLonPair:
    lat: float
    lon: float


@dataclasses.dataclass
class Error:
    lat_err: float
    lon_err: float


class Coordinates:
    def __init__(
        self,
        lat: float,
        lon: float,
        lat_err: float | None = None,
        lon_err: float | None = None,
    ):
        self.lat_lon_pair = LatLonPair(lat, lon)
        self.error = (
            Error(lat_err, lon_err)
            if lat_err is not None and lon_err is not None
            else None
        )

    def get_latitude(self) -> float:
        return self.lat_lon_pair.lat

    def get_longitude(self) -> float:
        return self.lat_lon_pair.lon

    def get_error(self) -> Error | None:
        return self.error

    def __str__(self):
        return f"{self.lat_lon_pair} | {self.error}"
