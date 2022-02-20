"""Project wide exception classes."""


class PrometheusApiClientException(Exception):
    """API client exception, raises when response status code != 200."""

    pass


class MetricValueConversionError(Exception):
    """Raises when we find a metric that is a string where we fail to convert it to a float."""

    pass
