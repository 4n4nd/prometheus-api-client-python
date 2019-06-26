"""docstring for MetricsList."""

from .metric import Metric


class MetricsList(list):
    """docstring for MetricsList."""

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
