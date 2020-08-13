"""A list of Metric objects."""

from .metric import Metric


class MetricsList(list):
    """A Class to initialize a list of Metric objects at once.

    :param metric_data_list: (list|json) This is an individual metric or list of metrics received
                             from prometheus as a result of a promql query.

    Example Usage:
      .. code-block:: python

          prom = PrometheusConnect()
          my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}
          metric_data = prom.get_metric_range_data(metric_name='up', label_config=my_label_config)

          metric_object_list = MetricsList(metric_data) # metric_object_list will be initialized as
                                                        # a list of Metric objects for all the
                                                        # metrics downloaded using get_metric query

    """

    def __init__(self, metric_data_list):
        """Class MetricsList constructor."""
        if not isinstance(metric_data_list, list):
            metric_data_list = [metric_data_list]

        metric_object_list = []

        def add_metric_to_object_list(metric):
            metric_object = Metric(metric)
            if metric_object in metric_object_list:
                metric_object_list[metric_object_list.index(metric_object)] += metric_object
            else:
                metric_object_list.append(metric_object)

        for i in metric_data_list:
            # If it is a list of lists (for example: while reading from multiple json files)
            if isinstance(i, list):
                for metric in i:
                    add_metric_to_object_list(metric)
            else:
                add_metric_to_object_list(i)

        super(MetricsList, self).__init__(metric_object_list)
