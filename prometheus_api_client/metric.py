"""A Class for metric object."""
from copy import deepcopy
import datetime
import pandas

try:
    import matplotlib.pyplot as plt
    from pandas.plotting import register_matplotlib_converters

    register_matplotlib_converters()
    _MPL_FOUND = True
except ImportError as exce:  # noqa F841
    _MPL_FOUND = False


class Metric:
    r"""
    A Class for `Metric` object.

    :param metric: (dict) A metric item from the list of metrics received from prometheus
    :param oldest_data_datetime: (datetime|timedelta) Any metric values in the dataframe that are
                    older than this value will be deleted when new data is added to the dataframe
                    using the __add__("+") operator.

                    * `oldest_data_datetime=datetime.timedelta(days=2)`, will delete the
                      metric data that is 2 days older than the latest metric.
                      The dataframe is pruned only when new data is added to it.
                    * `oldest_data_datetime=datetime.datetime(2019,5,23,12,0)`, will delete
                      any data that is older than "23 May 2019 12:00:00"
                    * `oldest_data_datetime=datetime.datetime.fromtimestamp(1561475156)`
                      can also be set using the unix timestamp

    Example Usage:
      .. code-block:: python

          prom = PrometheusConnect()

          my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}

          metric_data = prom.get_metric_range_data(metric_name='up', label_config=my_label_config)
          # Here metric_data is a list of metrics received from prometheus

          # only for the first item in the list
          my_metric_object = Metric(metric_data[0], datetime.timedelta(days=10))

    """

    def __init__(self, metric, oldest_data_datetime=None):
        """Functions as a Constructor for the Metric object."""
        if not isinstance(
            oldest_data_datetime, (datetime.datetime, datetime.timedelta, type(None))
        ):
            # if it is neither a datetime object nor a timedelta object raise exception
            raise TypeError(
                "oldest_data_datetime can only be datetime.datetime/ datetime.timedelta or None"
            )

        if isinstance(metric, Metric):
            # if metric is a Metric object, just copy the object and update its parameters
            self.metric_name = metric.metric_name
            self.label_config = metric.label_config
            self.metric_values = metric.metric_values
            self.oldest_data_datetime = oldest_data_datetime
        else:
            self.metric_name = metric["metric"]["__name__"]
            self.label_config = deepcopy(metric["metric"])
            self.oldest_data_datetime = oldest_data_datetime
            del self.label_config["__name__"]

            # if it is a single value metric change key name
            if "value" in metric:
                metric["values"] = [metric["value"]]

            self.metric_values = pandas.DataFrame(metric["values"], columns=["ds", "y"]).apply(
                pandas.to_numeric, errors="raise"
            )
            self.metric_values["ds"] = pandas.to_datetime(self.metric_values["ds"], unit="s")

        # Set the metric start time and the metric end time
        self.start_time = self.metric_values.iloc[0, 0]
        self.end_time = self.metric_values.iloc[-1, 0]

    def __eq__(self, other):
        """
        Overloading operator ``=``.

        Check whether two metrics are the same (are the same time-series regardless of their data)

        Example Usage:
          .. code-block:: python

              metric_1 = Metric(metric_data_1)

              metric_2 = Metric(metric_data_2)

              print(metric_1 == metric_2) # will print True if they belong to the same time-series

        :return: (bool) If two Metric objects belong to the same time-series,
                 i.e. same name and label config, it will return True, else False
        """
        return bool(
            (self.metric_name == other.metric_name) and (self.label_config == other.label_config)
        )

    def __str__(self):
        """
        Make it print in a cleaner way when print function is used on a Metric object.

        Example Usage:
          .. code-block:: python

              metric_1 = Metric(metric_data_1)

              print(metric_1) # will print the name, labels and the head of the dataframe

        """
        name = "metric_name: " + repr(self.metric_name) + "\n"
        labels = "label_config: " + repr(self.label_config) + "\n"
        values = "metric_values: " + repr(self.metric_values)

        return "{" + "\n" + name + labels + values + "\n" + "}"

    def __add__(self, other):
        r"""
        Overloading operator ``+``.

        Add two metric objects for the same time-series

        Example Usage:
          .. code-block:: python

            metric_1 = Metric(metric_data_1)
            metric_2 = Metric(metric_data_2)
            metric_12 = metric_1 + metric_2 # will add the data in ``metric_2`` to ``metric_1``
                                            # so if any other parameters are set in ``metric_1``
                                            # will also be set in ``metric_12``
                                            # (like ``oldest_data_datetime``)

        :return: (`Metric`) Returns a `Metric` object with the combined metric data
          of the two added metrics

        :raises: (TypeError) Raises an exception when two metrics being added are
          from different metric time-series
        """
        if self == other:
            new_metric = deepcopy(self)
            new_metric.metric_values = new_metric.metric_values.append(
                other.metric_values, ignore_index=True
            )
            new_metric.metric_values = new_metric.metric_values.dropna()
            new_metric.metric_values = (
                new_metric.metric_values.drop_duplicates("ds")
                .sort_values(by=["ds"])
                .reset_index(drop=True)
            )
            # if oldest_data_datetime is set, trim the dataframe and only keep the newer data
            if new_metric.oldest_data_datetime:
                if isinstance(new_metric.oldest_data_datetime, datetime.timedelta):
                    # create a time range mask
                    mask = new_metric.metric_values["ds"] >= (
                        new_metric.metric_values.iloc[-1, 0] - abs(new_metric.oldest_data_datetime)
                    )
                else:
                    # create a time range mask
                    mask = new_metric.metric_values["ds"] >= new_metric.oldest_data_datetime
                # truncate the df within the mask
                new_metric.metric_values = new_metric.metric_values.loc[mask]

            # Update the metric start time and the metric end time for the new Metric
            new_metric.start_time = new_metric.metric_values.iloc[0, 0]
            new_metric.end_time = new_metric.metric_values.iloc[-1, 0]

            return new_metric

        if self.metric_name != other.metric_name:
            error_string = "Different metric names"
        else:
            error_string = "Different metric labels"
        raise TypeError("Cannot Add different metric types. " + error_string)

    def plot(self):
        """Plot a very simple line graph for the metric time-series."""
        if _MPL_FOUND:
            fig, axis = plt.subplots()
            axis.plot_date(self.metric_values.ds, self.metric_values.y, linestyle=":")
            fig.autofmt_xdate()
        # if matplotlib was not imported
        else:
            raise ImportError("matplotlib was not found")
