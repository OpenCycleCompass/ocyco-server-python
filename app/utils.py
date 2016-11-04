from language_tags import tags


def is_valid_ietf_language(language):
    return tags.check(language)


def get_city_by_coordinates(lon, lat):
    # TODO: determinate city (reverse geocoding...)
    return "MyCity"
