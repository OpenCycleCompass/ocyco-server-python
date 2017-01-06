from language_tags import tags
from struct import unpack
from collections import namedtuple


def is_valid_ietf_language(language):
    return tags.check(language)


def get_city_by_coordinates(lon, lat):
    # TODO: determinate city (reverse geocoding...)
    return "MyCity"


def read_wkb_point(wkb):
    """ Read a WKB point.

    :param wkb: file-like object: Binary raster in WKB format
    :returns: obj: {'x': float, 'y': float}
    """

    # Determine the endiannes of the wkb
    (endian,) = unpack('<b', wkb[0:1])

    if endian == 0:
        endian = '>'
    elif endian == 1:
        endian = '<'

    # Read the wkb data.
    """
    WKB format:
    WKBPoint {
        byte       byteOrder;
        uint32     wkbType;  // == 1
        Point      point;
    }
    Point {
        double x;
        double y;
    };
    """
    (wkb_type, x, y) = unpack(endian + 'Ldd', wkb[1:21])

    if wkb_type != 1:
        raise ValueError('WKB object is not a point.')

    geo_point = namedtuple('Point', 'x y')
    return geo_point(x, y)
