"""A collection of tools to collect and manipulate prometheus metrics."""

__title__ = "prometheus-connect"
__version__ = "0.7.0"

from .exceptions import PrometheusApiClientException, MetricValueConversionError
def __getattr__(name):
    if name == "PrometheusConnect":
        from .prometheus_connect import PrometheusConnect
        return PrometheusConnect
    elif name == "Metric":
        from .metric import Metric
        return Metric
    elif name == "MetricsList":
        from .metrics_list import MetricsList
        return MetricsList
    elif name == "MetricSnapshotDataFrame":
        from .metric_snapshot_df import MetricSnapshotDataFrame
        return MetricSnapshotDataFrame
    elif name == "MetricRangeDataFrame":
        from .metric_range_df import MetricRangeDataFrame
        return MetricRangeDataFrame
    raise AttributeError(f"module {__name__} has no attribute {name}")
