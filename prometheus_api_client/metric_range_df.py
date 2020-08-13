"""A pandas.DataFrame subclass for Prometheus range vector responses."""
from pandas import DataFrame
from pandas._typing import Axes, Dtype
from typing import Optional, Sequence


class MetricRangeDataFrame(DataFrame):
    """Subclass to format and represent Prometheus query response as pandas.DataFrame.

    Assumes response is either a json or sequence of jsons.

    This class should be used specifically to instantiate a query response,
    where the query response has several timestamp values per series.
    That is, a range vector is expected.
    If the data is an instant vector, use MetricSnapshotDataFrame instead.

    Some argument descriptions in this docstring were copied from pandas.core.frame.DataFrame.

    :param data: (list|json) A single metric (json with keys "metric" and "values"/"value")
        or list of such metrics received from Prometheus as a response to query
    :param index: (pandas.Index|array-like) Index to use for resulting dataframe. Will default to
                 pandas.RangeIndex if no indexing information part of input data and no index provided.
    :param columns: (pandas.Index|array-like) Column labels to use for resulting dataframe. Will
                 default to list of labels + "timestamp" + "value" if not provided.
    :param dtype: (dtype) default None. Data type to force. Only a single dtype is allowed. If None, infer.
    :param copy: (bool) default False. Copy data from inputs. Only affects DataFrame / 2d ndarray input.

    Example Usage:
      .. code-block:: python

          prom = PrometheusConnect()
          metric_data = prom.get_current_metric_value(metric_name='up', label_config=my_label_config)
          metric_df = MetricRangeDataFrame(metric_data)
          metric_df.head()
          '''
          +------------+------------+-----------------+--------------------+-------+
          |            |  __name__  | cluster         | label_2            | value |
          +-------------------------+-----------------+--------------------+-------+
          | timestamp  |            |                 |                    |       |
          +============+============+=================+====================+=======+
          | 1577836800 |   __up__   | cluster_id_0    | label_2_value_2    | 0     |
          +-------------------------+-----------------+--------------------+-------+
          | 1577836801 |   __up__   | cluster_id_1    | label_2_value_3    | 1     |
          +-------------------------+-----------------+------------=-------+-------+
          '''
    """

    def __init__(
        self,
        data=None,
        index: Optional[Axes] = None,
        columns: Optional[Axes] = None,
        dtype: Optional[Dtype] = None,
        copy: bool = False,
    ):
        """Functions as a constructor for MetricRangeDataFrame class."""
        if data is not None:
            # if just a single json instead of list/set/other sequence of jsons,
            # treat as list with single entry
            if not isinstance(data, Sequence):
                data = [data]

        row_data = []
        for v in data:
            if "value" in v:
                raise TypeError(
                    "data must be a range vector. Expected range vector, got instant vector"
                )
            for t in v["values"]:
                row_data.append({**v["metric"], "timestamp": t[0], "value": t[1]})

        # init df normally now
        super(MetricRangeDataFrame, self).__init__(
            data=row_data, index=index, columns=columns, dtype=dtype, copy=copy
        )

        self.set_index(["timestamp"], inplace=True)
