class Coordinates:
    """
    Create polygon.Coordinates at the specified latitude and longitude.
    """

    # todo use properties

    def __init__(
        self,
        lat: float,
        lon: float,
        lat_err: float | None = None,
        lon_err: float | None = None,
    ):
        """
        Args:
           lat: Latitude for this coordinate pair, in degrees.
           lon: Longitude for this coordinate pair, in degrees.
        """
        self.lat_lon_pair = LatLonPair(lat, lon)
        self.error = Error(lat_err, lon_err)

    def getLatitude(self):
        return self.lat_lon_pair.getLat()

    def getLongitude(self):
        return self.lat_lon_pair.getLon()

    def getError(self):
        return self.error

    def __str__(self):
        return f"{self.lat_lon_pair} | {self.error}"


class LatLonPair:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def getLon(self) -> float:
        return self.lon

    def getLat(self) -> float:
        return self.lat

    def __str__(self) -> str:
        return f"{self.lat} | {self.lon}"


class Error:
    def __init__(self, lat: float, lon: float):
        self.lat_lon_pair = LatLonPair(lat, lon)

    def getLon(self) -> float:
        return self.lat_lon_pair.lon

    def getLat(self) -> float:
        return self.lat_lon_pair.lat

    def __str__(self) -> str:
        return f"{self.lat_lon_pair.lat} | {self.lat_lon_pair.lon}"
