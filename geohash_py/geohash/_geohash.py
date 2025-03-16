"""
INSPIRED FROM
https://github.com/joyanujoy/geolib/blob/master/geolib/geohash.py

# todo change named tuples to data classes

Geohash encoding/decoding and associated functions
(c) Chris Veness 2014-2016 / MIT Licence
https://www.movable-type.co.uk/scripts/geohash.html

http://en.wikipedia.org/wiki/Geohash
"""

from __future__ import division

import decimal
import math
from builtins import range
from collections import namedtuple

__base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
__decodemap = {}
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i
del i


def _indexes(geohash: str):
    if not geohash:
        raise ValueError("Invalid geohash")

    for char in geohash:
        try:
            yield __base32.index(char)
        except ValueError:
            raise ValueError("Invalid geohash")


def _fixedpoint(num, bound_max, bound_min):
    """
    Return given num with precision of 2 - log10(range)

    Params
    ------
    num: A number
    bound_max: max bound, e.g max latitude of a geohash cell(NE)
    bound_min: min bound, e.g min latitude of a geohash cell(SW)

    Returns
    -------
    A decimal
    """
    try:
        decimal.getcontext().prec = math.floor(2 - math.log10(bound_max - bound_min))
    except ValueError:
        decimal.getcontext().prec = 12
    return decimal.Decimal(num)


def bounds(geohash: str) -> namedtuple:
    """
    Returns SW/NE latitude/longitude bounds of a specified geohash::

            |      .| NE
            |    .  |
            |  .    |
         SW |.      |

    :param geohash: string, cell that bounds are required of

    :returns: a named tuple of namedtuples Bounds(sw(lat, lon), ne(lat, lon)).

    >>> bounds = geohash.bounds('ezs42')
    >>> bounds
    >>> ((42.583, -5.625), (42.627, -5.58)))
    >>> bounds.sw.lat
    >>> 42.583

    """
    geohash = geohash.lower()

    even_bit = True
    lat_min = -90
    lat_max = 90
    lon_min = -180
    lon_max = 180

    # 5 bits for a char. So divide the decimal by power of 2, then AND 1
    # to get the binary bit - fast modulo operation.
    for index in _indexes(geohash):
        for n in range(4, -1, -1):
            bit = (index >> n) & 1
            if even_bit:
                # longitude
                lon_mid = (lon_min + lon_max) / 2
                if bit == 1:
                    lon_min = lon_mid
                else:
                    lon_max = lon_mid
            else:
                # latitude
                lat_mid = (lat_min + lat_max) / 2
                if bit == 1:
                    lat_min = lat_mid
                else:
                    lat_max = lat_mid
            even_bit = not even_bit

    SouthWest = namedtuple("SouthWest", ["lat", "lon"])
    NorthEast = namedtuple("NorthEast", ["lat", "lon"])
    sw = SouthWest(lat_min, lon_min)
    ne = NorthEast(lat_max, lon_max)
    Bounds = namedtuple("Bounds", ["sw", "ne"])
    return Bounds(sw, ne)


def decode_exactly(geohash):
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    lat_err, lon_err = 90.0, 180.0
    is_even = True
    for c in geohash:
        cd = __decodemap[c]
        for mask in [16, 8, 4, 2, 1]:
            if is_even:  # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval = (
                        (lon_interval[0] + lon_interval[1]) / 2,
                        lon_interval[1],
                    )
                else:
                    lon_interval = (
                        lon_interval[0],
                        (lon_interval[0] + lon_interval[1]) / 2,
                    )
            else:  # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval = (
                        (lat_interval[0] + lat_interval[1]) / 2,
                        lat_interval[1],
                    )
                else:
                    lat_interval = (
                        lat_interval[0],
                        (lat_interval[0] + lat_interval[1]) / 2,
                    )
            is_even = not is_even
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    return lat, lon, lat_err, lon_err


def decode(geohash):
    """
    Decode geohash, returning two strings with latitude and longitude
    containing only relevant digits and with trailing zeroes removed.
    """
    lat, lon, lat_err, lon_err = decode_exactly(geohash)
    # Format to the number of decimals that are known
    lats = "%.*f" % (max(1, int(round(-math.log10(lat_err)))) - 1, lat)
    lons = "%.*f" % (max(1, int(round(-math.log10(lon_err)))) - 1, lon)
    if "." in lats:
        lats = lats.rstrip("0")
    if "." in lons:
        lons = lons.rstrip("0")
    return lats, lons


'''

def decode(geohash):
    """
    Decode geohash to latitude/longitude. Location is approximate centre of the
    cell to reasonable precision.

    :param geohash: string, cell that bounds are required of

    :returns: Namedtuple with decimal lat and lon as properties.

    >>> geohash.decode('gkkpfve')
    >>> (70.2995, -27.9993)
    """
    (lat_min, lon_min), (lat_max, lon_max) = bounds(geohash)

    lat = (lat_min + lat_max) / 2
    lon = (lon_min + lon_max) / 2

    lat = _fixedpoint(lat, lat_max, lat_min)
    lon = _fixedpoint(lon, lon_max, lon_min)
    Point = namedtuple('Point', ['lat', 'lon'])
    return Point(lat, lon)
'''


def encode(lat, lon, precision):
    """
    Encode latitude, longitude to a geohash.

    :param lat: latitude, a number or string that can be converted to decimal.
         Ideally pass a string to avoid floating point uncertainties.
         It will be converted to decimal.
    :param lon: longitude, a number or string that can be converted to decimal.
         Ideally pass a string to avoid floating point uncertainties.
         It will be converted to decimal.
    :param precision: integer, 1 to 12 represeting geohash levels upto 12.

    :returns: geohash as string.

    >>> geohash.encode('70.2995', '-27.9993', 7)
    >>> gkkpfve
    """
    lat = decimal.Decimal(lat)
    lon = decimal.Decimal(lon)

    index = 0  # index into base32 map
    bit = 0  # each char holds 5 bits
    even_bit = True
    lat_min = -90
    lat_max = 90
    lon_min = -180
    lon_max = 180
    ghash = []

    while len(ghash) < precision:
        if even_bit:
            # bisect E-W longitude
            lon_mid = (lon_min + lon_max) / 2
            if lon >= lon_mid:
                index = index * 2 + 1
                lon_min = lon_mid
            else:
                index = index * 2
                lon_max = lon_mid
        else:
            # bisect N-S latitude
            lat_mid = (lat_min + lat_max) / 2
            if lat >= lat_mid:
                index = index * 2 + 1
                lat_min = lat_mid
            else:
                index = index * 2
                lat_max = lat_mid
        even_bit = not even_bit

        bit += 1
        if bit == 5:
            # 5 bits gives a char in geohash. Start over
            ghash.append(__base32[index])
            bit = 0
            index = 0

    return "".join(ghash)


def adjacent(geohash, direction):
    """
    Determines adjacent cell in given direction.

    :param geohash: cell to which adjacent cell is required
    :param direction: direction from geohash, string, one of n, s, e, w

    :returns: geohash of adjacent cell

    >>> geohash.adjacent('gcpuyph', 'n')
    >>> gcpuypk
    """
    if not geohash:
        raise ValueError("Invalid geohash")
    if direction not in ("nsew"):
        raise ValueError("Invalid direction")

    neighbour = {
        "n": ["p0r21436x8zb9dcf5h7kjnmqesgutwvy", "bc01fg45238967deuvhjyznpkmstqrwx"],
        "s": ["14365h7k9dcfesgujnmqp0r2twvyx8zb", "238967debc01fg45kmstqrwxuvhjyznp"],
        "e": ["bc01fg45238967deuvhjyznpkmstqrwx", "p0r21436x8zb9dcf5h7kjnmqesgutwvy"],
        "w": ["238967debc01fg45kmstqrwxuvhjyznp", "14365h7k9dcfesgujnmqp0r2twvyx8zb"],
    }

    border = {
        "n": ["prxz", "bcfguvyz"],
        "s": ["028b", "0145hjnp"],
        "e": ["bcfguvyz", "prxz"],
        "w": ["0145hjnp", "028b"],
    }

    last_char = geohash[-1]
    parent = geohash[:-1]  # parent is hash without last char

    typ = len(geohash) % 2

    # check for edge-cases which don't share common prefix
    if last_char in border[direction][typ] and parent:
        parent = adjacent(parent, direction)

    index = neighbour[direction][typ].index(last_char)
    return parent + __base32[index]


def neighbors(geohash: str) -> namedtuple:
    """
    Returns all 8 adjacent cells to specified geohash::

        | nw | n | ne |
        |  w | * | e  |
        | sw | s | se |

    :param geohash: string, geohash neighbours are required of

    :returns: neighbours as namedtuple of geohashes with properties n,ne,e,se,s,sw,w,nw

    >>> neighbours = geohash.neighbors('gcpuyph')
    >>> neighbours
    >>> ('gcpuypk', 'gcpuypm', 'gcpuypj', 'gcpuynv', 'gcpuynu', 'gcpuyng', 'gcpuyp5', 'gcpuyp7')
    >>> neighbours.ne
    >>> gcpuypm
    """
    n = adjacent(geohash, "n")
    ne = adjacent(n, "e")
    e = adjacent(geohash, "e")
    s = adjacent(geohash, "s")
    se = adjacent(s, "e")
    w = adjacent(geohash, "w")
    sw = adjacent(s, "w")
    nw = adjacent(n, "w")
    Neighbours = namedtuple("Neighbours", ["n", "ne", "e", "se", "s", "sw", "w", "nw"])
    return Neighbours(n, ne, e, se, s, sw, w, nw)
