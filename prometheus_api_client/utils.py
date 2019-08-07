"""
Some helpful functions used in the API
"""
import dateparser


def parse_datetime(date_string: str, settings: dict = None):
    """
    A wrapper for dateparser.parse, but the default settings are set
    to {"DATE_ORDER": "YMD"}
    """

    settings = settings or {"DATE_ORDER": "YMD"}
    return dateparser.parse(str(date_string), settings=settings)


def parse_timedelta(time_a: str = "now", time_b: str = "1d"):
    """
    returns timedelta for time_a - time_b
    """
    return parse_datetime(time_a) - parse_datetime(time_b)
