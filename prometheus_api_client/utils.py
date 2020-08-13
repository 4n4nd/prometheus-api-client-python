"""Some helpful functions used in the API."""
import json
import dateparser


def parse_datetime(date_string: str, settings: dict = None):
    """Functions as a wrapper for dateparser.parse, but the default settings are set to {"DATE_ORDER": "YMD"}."""
    settings = settings or {"DATE_ORDER": "YMD"}
    return dateparser.parse(str(date_string), settings=settings)


def parse_timedelta(time_a: str = "now", time_b: str = "1d"):
    """Return timedelta for time_a - time_b."""
    return parse_datetime(time_a) - parse_datetime(time_b)


def pretty_print_metric(metric_data):
    """
    Pretty print the metric data downloaded using class PrometheusConnect.

    :param metric_data: (list) This is the metric data list returned from methods
        get_metric_range_data and get_current_metric_value
    """
    data = metric_data
    for metric in data:
        print(json.dumps(metric, indent=4, sort_keys=True))
