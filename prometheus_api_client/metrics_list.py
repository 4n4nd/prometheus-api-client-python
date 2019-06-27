"""docstring for MetricsList."""

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
        # if the input is not a list
        if not isinstance(metric_data_list, list):
            # make it into a list
            metric_data_list = [metric_data_list]

        metric_object_list = []
        for i in metric_data_list:
            metric_object = Metric(i)
            if metric_object in metric_object_list:
                metric_object_list[metric_object_list.index(metric_object)] += metric_object
            else:
                metric_object_list.append(metric_object)
        super(MetricsList, self).__init__(metric_object_list)
