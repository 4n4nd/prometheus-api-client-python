"""Project wide exception classes."""


class PrometheusApiClientException(Exception):
    """API client exception, raises when response status code != 200."""

    pass
