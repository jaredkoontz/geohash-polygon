from dataclasses import dataclass

from geohash_poly.coordinates import Coordinates


@dataclass
class PolygonInfo:
    """Class for keeping track of an item in inventory."""

    coords: list[Coordinates]
    leh: str
    num_hashes: int


us = PolygonInfo(
    [
        Coordinates(28.22697003891834, -123.662109375),
        Coordinates(50.42951794712287, -123.662109375),
        Coordinates(50.42951794712287, -90.04394531249999),
        Coordinates(28.22697003891834, -90.0439453124999),
    ],
    "",
    12,
)

wyoming_co = PolygonInfo(
    [
        Coordinates(44.99588261816546, -109.248046875),
        Coordinates(38.238180119798635, -109.1162109375),
        Coordinates(38.41055825094609, -102.8320312),
    ],
    "9",
    15,
)

no_co = PolygonInfo(
    [
        Coordinates(39.56758783088903, -106.1444091796875),
        Coordinates(40.942564441333296, -106.1444091796875),
        Coordinates(40.942564441333296, -103.88671875),
        Coordinates(39.56758783088903, -103.8867187),
    ],
    "9x",
    56,
)

weird = PolygonInfo(
    [
        Coordinates(40.6639728763869, -105.0567626953125),
        Coordinates(40.49918094806632, -105.38360595703125),
        Coordinates(40.0717663466261, -104.4854736328125),
        Coordinates(40.29419163838167, -104.47448730468749),
        Coordinates(40.30466538259176, -104.765625),
        Coordinates(40.47202439692057, -104.6392822265625),
        Coordinates(40.46575594018434, -104.9441528320312),
    ],
    "9xj",
    92,
)
