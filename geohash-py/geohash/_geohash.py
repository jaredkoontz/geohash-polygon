BITS_PER_CHAR = 5
LATITUDE_RANGE = 90
LONGITUDE_RANGE = 180

CHAR_MAP = [
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c',
			'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r',
			's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
	]

CHAR_LOOKUP_TABLE = {CHAR_MAP[i]:i for i in range(len(CHAR_MAP))}

DEFAULT_PRECISION = 12

def encode()
