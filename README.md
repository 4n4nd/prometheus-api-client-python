# prometheus-api-client

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7d838be9b51e4daaa20be1772f5c9ad2)](https://www.codacy.com/manual/4n4nd/prometheus-api-client-python?utm_source=github.com&utm_medium=referral&utm_content=AICoE/prometheus-api-client-python&utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/prometheus-api-client.svg)](https://badge.fury.io/py/prometheus-api-client) [![PyPI download month](https://img.shields.io/pypi/dm/prometheus-api-client.svg)](https://pypi.python.org/pypi/prometheus-api-client/)

A Python wrapper for the Prometheus http api and some tools for metrics processing.

## Installation

To install the latest release:

`pip install prometheus-api-client`

To install directly from this branch:

`pip install https://github.com/AICoE/prometheus-api-client-python/zipball/master`

## Links

- [Slack](https://join.slack.com/share/zt-kw3v8t1e-hbcVH7X7bXORiQuQtsNZ4A)
- [Google Chat](https://chat.google.com/room/AAAAzFPwq5s)
- [Documentation](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html)

## Getting Started

### Usage
[Prometheus](https://prometheus.io/), a Cloud Native Computing Foundation project, is a systems and service monitoring system. It collects metrics (time series data) from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true. The raw time series data obtained from a Prometheus host can sometimes be hard to interpret. To help better understand these metrics we have created a Python wrapper for the Prometheus http api for easier metrics processing and analysis.

The `prometheus-api-client` library consists of multiple modules which assist in connecting to a Prometheus host, fetching the required metrics and performing various aggregation operations on the time series data.

#### Connecting and Collecting Metrics from a Prometheus host
The `PrometheusConnect` module of the library can be used to connect to a Prometheus host. This module is essentially a class created for the collection of metrics from a Prometheus host. It stores the following connection parameters:

-   **url** - (str) url for the prometheus host
-   **headers** – (dict) A dictionary of http headers to be used to communicate with the host. Example: {“Authorization”: “bearer my_oauth_token_to_the_host”}
-   **disable_ssl** – (bool) If set to True, will disable ssl certificate verification for the http requests made to the prometheus host

```python
from prometheus_api_client import PrometheusConnect
prom = PrometheusConnect(url ="<prometheus-host>", disable_ssl=True)

# Get the list of all the metrics that the Prometheus host scrapes
prom.all_metrics()
```

You can also fetch the time series data for a specific metric using custom queries as follows:

```python
prom = PrometheusConnect()
my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}
prom.get_current_metric_value(metric_name='up', label_config=my_label_config)

# Here, we are fetching the values of a particular metric name
prom.custom_query(query="prometheus_http_requests_total")

# Now, lets try to fetch the `sum` of the metrics
prom.custom_query(query="sum(prometheus_http_requests_total)")
```

We can also use custom queries for fetching the metric data in a specific time interval. For example, let's try to fetch the past 2 days of data for a particular metric in chunks of 1 day:

```python
# Import the required datetime functions
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta

start_time = parse_datetime("2d")
end_time = parse_datetime("now")
chunk_size = timedelta(days=1)

metric_data = prom.get_metric_range_data(
    "up{cluster='my_cluster_id'}",  # this is the metric name and label config
    start_time=start_time,
    end_time=end_time,
    chunk_size=chunk_size,
)
```

For more functions included in the `PrometheusConnect` module, refer to this [documentation.](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html#module-prometheus_api_client.prometheus_connect)

#### Understanding the Metrics Data Fetched
The `MetricsList` module initializes a list of Metric objects for the metrics fetched from a Prometheus host as a result of a promql query.

```python
# Import the MetricsList and Metric modules
from prometheus_api_client import PrometheusConnect, MetricsList, Metric

prom = PrometheusConnect()
my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}
metric_data = prom.get_metric_range_data(metric_name='up', label_config=my_label_config)

metric_object_list = MetricsList(metric_data) # metric_object_list will be initialized as
                                              # a list of Metric objects for all the
                                              # metrics downloaded using get_metric query

# We can see what each of the metric objects look like
for item in metric_object_list:
    print(item.metric_name, item.label_config, "\n")
```

Each of the items in the `metric_object_list` are initialized as a `Metric` class object. Let's look at one of the metrics from the `metric_object_list` to learn more about the `Metric` class:

```python
my_metric_object = metric_object_list[1] # one of the metrics from the list
print(my_metric_object)
```

For more functions included in the `MetricsList` and `Metrics` module, refer to this [documentation.](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html#module-prometheus_api_client.metric)

#### Additional Metric Functions
The `Metric` class also supports multiple functions such as adding, equating and plotting various metric objects.

##### Adding Metrics
You can add add two metric objects for the same time-series as follows:

```python
metric_1 = Metric(metric_data_1)
metric_2 = Metric(metric_data_2)
metric_12 = metric_1 + metric_2 # will add the data in ``metric_2`` to ``metric_1``
                                # so if any other parameters are set in ``metric_1``
                                # will also be set in ``metric_12``
                                # (like ``oldest_data_datetime``)
```

##### Equating Metrics
Overloading operator =, to check whether two metrics are the same (are the same time-series regardless of their data)
```python
metric_1 = Metric(metric_data_1)
metric_2 = Metric(metric_data_2)
print(metric_1 == metric_2) # will print True if they belong to the same time-series
```

##### Plotting Metric Objects
Plot a very simple line graph for the metric time series:

```python
from prometheus_api_client import PrometheusConnect, MetricsList, Metric

prom = PrometheusConnect()
my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}
metric_data = prom.get_metric_range_data(metric_name='up', label_config=my_label_config)

metric_object_list = MetricsList(metric_data)
my_metric_object = metric_object_list[1] # one of the metrics from the list
my_metric_object.plot()
```

#### Getting Metrics Data as pandas DataFrames
To perform data analysis and manipulation, it is often helpful to have the data represented using a [pandas DataFrame](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe). There are two modules in this library that can be used to process the raw metrics fetched into a DataFrame.

The `MetricSnapshotDataFrame` module converts "current metric value" data to a DataFrame representation, and the `MetricRangeDataFrame` converts "metric range values" data to a DataFrame representation. Example usage of these classes can be seen below:

```python
import datetime as dt
from prometheus_api_client import PrometheusConnect,  MetricSnapshotDataFrame, MetricRangeDataFrame

prom = PrometheusConnect()
my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}

# metric current values
metric_data = prom.get_current_metric_value(
    metric_name='up',
    label_config=my_label_config,
)
metric_df = MetricSnapshotDataFrame(metric_data)
metric_df.head()
""" Output:
+-------------------------+-----------------+------------+-------+
| __name__ | cluster      | label_2         | timestamp  | value |
+==========+==============+=================+============+=======+
| up       | cluster_id_0 | label_2_value_2 | 1577836800 | 0     |
+-------------------------+-----------------+------------+-------+
| up       | cluster_id_1 | label_2_value_3 | 1577836800 | 1     |
+-------------------------+-----------------+------------+-------+
"""

# metric values for a range of timestamps
metric_data = prom.get_metric_range_data(
    metric_name='up',
    label_config=my_label_config,
    start_time=(dt.datetime.now() - dt.timedelta(minutes=30)),
    end_time=dt.datetime.now(),
)
metric_df = MetricRangeDataFrame(metric_data)
metric_df.head()
""" Output:
+------------+------------+-----------------+--------------------+-------+
|            |  __name__  | cluster         | label_2            | value |
+-------------------------+-----------------+--------------------+-------+
| timestamp  |            |                 |                    |       |
+============+============+=================+====================+=======+
| 1577836800 | up         | cluster_id_0    | label_2_value_2    | 0     |
+-------------------------+-----------------+--------------------+-------+
| 1577836801 | up         | cluster_id_1    | label_2_value_3    | 1     |
+-------------------------+-----------------+------------=-------+-------+
"""
```


For more functions included in the `prometheus-api-client` library, please refer to this [documentation.](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html)

## Running tests

`PROM_URL="http://demo.robustperception.io:9090/" pytest`

## Code Styling and Linting

Prometheus Api client uses [pre-commit](https://pre-commit.com) framework to maintain the code linting and python code styling.<br>
The AICoE-CI would run the pre-commit check on each pull request.<br>
We encourage our contributors to follow the same pattern, while contributing to the code.<br>
we would like to keep the same standard and maintain the code for better quality and readability.

The pre-commit configuration file is present in the repository `.pre-commit-config.yaml`<br>
It contains the different code styling and linting guide which we use for the application.

we just need to run [pre-commit](https://pre-commit.com/#install) before raising a Pull Request.<br>
Following command can be used to run the pre-commit:<br>
`pre-commit run --all-files`

If pre-commit is not installed in your system, it can be install with : `pip install pre-commit`
