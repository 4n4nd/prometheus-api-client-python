"""A Class for collection of metrics from a Prometheus Host."""
from urllib.parse import urlparse
import bz2
import os
import json
import logging
import numpy
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .exceptions import PrometheusApiClientException

# set up logging

_LOGGER = logging.getLogger(__name__)

# In case of a connection failure try 2 more times
MAX_REQUEST_RETRIES = 3
# wait 1 second before retrying in case of an error
RETRY_BACKOFF_FACTOR = 1
# retry only on these status
RETRY_ON_STATUS = [408, 429, 500, 502, 503, 504]


class PrometheusConnect:
    """
    A Class for collection of metrics from a Prometheus Host.

    :param url: (str) url for the prometheus host
    :param headers: (dict) A dictionary of http headers to be used to communicate with
        the host. Example: {"Authorization": "bearer my_oauth_token_to_the_host"}
    :param disable_ssl: (bool) If set to True, will disable ssl certificate verification
        for the http requests made to the prometheus host
    :param retry: (Retry) Retry adapter to retry on HTTP errors
    """

    def __init__(
        self,
        url: str = "http://127.0.0.1:9090",
        headers: dict = None,
        disable_ssl: bool = False,
        retry: Retry = None,
    ):
        """Functions as a Constructor for the class PrometheusConnect."""
        if url is None:
            raise TypeError("missing url")

        self.headers = headers
        self.url = url
        self.prometheus_host = urlparse(self.url).netloc
        self._all_metrics = None
        self.ssl_verification = not disable_ssl

        if retry is None:
            retry = Retry(
                total=MAX_REQUEST_RETRIES,
                backoff_factor=RETRY_BACKOFF_FACTOR,
                status_forcelist=RETRY_ON_STATUS,
            )

        self._session = requests.Session()
        self._session.mount(self.url, HTTPAdapter(max_retries=retry))

    def check_prometheus_connection(self, params: dict = None) -> bool:
        """
        Check Promethus connection.

        :param params: (dict) Optional dictionary containing parameters to be
            sent along with the API request.
        :returns: (bool) True if the endpoint can be reached, False if cannot be reached.
        """
        response = self._session.get(
            "{0}/".format(self.url),
            verify=self.ssl_verification,
            headers=self.headers,
            params=params,
        )
        return response.ok

    def all_metrics(self, params: dict = None):
        """
        Get the list of all the metrics that the prometheus host scrapes.

        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :returns: (list) A list of names of all the metrics available from the
            specified prometheus host
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code
        """
        params = params or {}
        response = self._session.get(
            "{0}/api/v1/label/__name__/values".format(self.url),
            verify=self.ssl_verification,
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            self._all_metrics = response.json()["data"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )
        return self._all_metrics

    def get_current_metric_value(
        self, metric_name: str, label_config: dict = None, params: dict = None
    ):
        r"""
        Get the current metric value for the specified metric and label configuration.

        :param metric_name: (str) The name of the metric
        :param label_config: (dict) A dictionary that specifies metric labels and their
            values
        :param params: (dict) Optional dictionary containing GET parameters to be sent
            along with the API request, such as "time"
        :returns: (list) A list of current metric values for the specified metric
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code

        Example Usage:
          .. code-block:: python

              prom = PrometheusConnect()

              my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}

              prom.get_current_metric_value(metric_name='up', label_config=my_label_config)
        """
        params = params or {}
        data = []
        if label_config:
            label_list = [str(key + "=" + "'" + label_config[key] + "'") for key in label_config]
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        # using the query API to get raw data
        response = self._session.get(
            "{0}/api/v1/query".format(self.url),
            params={**{"query": query}, **params},
            verify=self.ssl_verification,
            headers=self.headers,
        )

        if response.status_code == 200:
            data += response.json()["data"]["result"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )
        return data

    def get_metric_range_data(
        self,
        metric_name: str,
        label_config: dict = None,
        start_time: datetime = (datetime.now() - timedelta(minutes=10)),
        end_time: datetime = datetime.now(),
        chunk_size: timedelta = None,
        store_locally: bool = False,
        params: dict = None,
    ):
        r"""
        Get the current metric value for the specified metric and label configuration.

        :param metric_name: (str) The name of the metric.
        :param label_config: (dict) A dictionary specifying metric labels and their
            values.
        :param start_time:  (datetime) A datetime object that specifies the metric range start time.
        :param end_time: (datetime) A datetime object that specifies the metric range end time.
        :param chunk_size: (timedelta) Duration of metric data downloaded in one request. For
            example, setting it to timedelta(hours=3) will download 3 hours worth of data in each
            request made to the prometheus host
        :param store_locally: (bool) If set to True, will store data locally at,
            `"./metrics/hostname/metric_date/name_time.json.bz2"`
        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :return: (list) A list of metric data for the specified metric in the given time
            range
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code

        """
        params = params or {}
        data = []

        _LOGGER.debug("start_time: %s", start_time)
        _LOGGER.debug("end_time: %s", end_time)
        _LOGGER.debug("chunk_size: %s", chunk_size)

        if not (isinstance(start_time, datetime) and isinstance(end_time, datetime)):
            raise TypeError("start_time and end_time can only be of type datetime.datetime")

        if not chunk_size:
            chunk_size = end_time - start_time
        if not isinstance(chunk_size, timedelta):
            raise TypeError("chunk_size can only be of type datetime.timedelta")

        start = round(start_time.timestamp())
        end = round(end_time.timestamp())

        if end_time < start_time:
            raise ValueError("end_time must not be before start_time")

        if (end_time - start_time).total_seconds() < chunk_size.total_seconds():
            raise ValueError("specified chunk_size is too big")
        chunk_seconds = round(chunk_size.total_seconds())

        if label_config:
            label_list = [str(key + "=" + "'" + label_config[key] + "'") for key in label_config]
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name
        _LOGGER.debug("Prometheus Query: %s", query)

        while start < end:
            if start + chunk_seconds > end:
                chunk_seconds = end - start

            # using the query API to get raw data
            response = self._session.get(
                "{0}/api/v1/query".format(self.url),
                params={
                    **{
                        "query": query + "[" + str(chunk_seconds) + "s" + "]",
                        "time": start + chunk_seconds,
                    },
                    **params,
                },
                verify=self.ssl_verification,
                headers=self.headers,
            )
            if response.status_code == 200:
                data += response.json()["data"]["result"]
            else:
                raise PrometheusApiClientException(
                    "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
                )
            if store_locally:
                # store it locally
                self._store_metric_values_local(
                    metric_name,
                    json.dumps(response.json()["data"]["result"]),
                    start + chunk_seconds,
                )

            start += chunk_seconds
        return data

    def _store_metric_values_local(self, metric_name, values, end_timestamp, compressed=False):
        r"""
        Store metrics on the local filesystem, optionally  with bz2 compression.

        :param metric_name: (str) the name of the metric being saved
        :param values: (str) metric data in JSON string format
        :param end_timestamp: (int) timestamp in any format understood by \
            datetime.datetime.fromtimestamp()
        :param compressed: (bool) whether or not to apply bz2 compression
        :returns: (str) path to the saved metric file
        """
        if not values:
            _LOGGER.debug("No values for %s", metric_name)
            return None

        file_path = self._metric_filename(metric_name, end_timestamp)

        if compressed:
            payload = bz2.compress(str(values).encode("utf-8"))
            file_path = file_path + ".bz2"
        else:
            payload = str(values).encode("utf-8")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(payload)

        return file_path

    def _metric_filename(self, metric_name: str, end_timestamp: int):
        r"""
        Add a timestamp to the filename before it is stored.

        :param metric_name: (str) the name of the metric being saved
        :param end_timestamp: (int) timestamp in any format understood by \
            datetime.datetime.fromtimestamp()
        :returns: (str) the generated path
        """
        end_time_stamp = datetime.fromtimestamp(end_timestamp)
        directory_name = end_time_stamp.strftime("%Y%m%d")
        timestamp = end_time_stamp.strftime("%Y%m%d%H%M")
        object_path = (
            "./metrics/"
            + self.prometheus_host
            + "/"
            + metric_name
            + "/"
            + directory_name
            + "/"
            + timestamp
            + ".json"
        )
        return object_path

    def custom_query(self, query: str, params: dict = None):
        """
        Send a custom query to a Prometheus Host.

        This method takes as input a string which will be sent as a query to
        the specified Prometheus Host. This query is a PromQL query.

        :param query: (str) This is a PromQL query, a few examples can be found
            at https://prometheus.io/docs/prometheus/latest/querying/examples/
        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :returns: (list) A list of metric data received in response of the query sent
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code
        """
        params = params or {}
        data = None
        query = str(query)
        # using the query API to get raw data
        response = self._session.get(
            "{0}/api/v1/query".format(self.url),
            params={**{"query": query}, **params},
            verify=self.ssl_verification,
            headers=self.headers,
        )
        if response.status_code == 200:
            data = response.json()["data"]["result"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )

        return data

    def custom_query_range(
        self, query: str, start_time: datetime, end_time: datetime, step: str, params: dict = None
    ):
        """
        Send a query_range to a Prometheus Host.

        This method takes as input a string which will be sent as a query to
        the specified Prometheus Host. This query is a PromQL query.

        :param query: (str) This is a PromQL query, a few examples can be found
            at https://prometheus.io/docs/prometheus/latest/querying/examples/
        :param start_time: (datetime) A datetime object that specifies the query range start time.
        :param end_time: (datetime) A datetime object that specifies the query range end time.
        :param step: (str) Query resolution step width in duration format or float number of seconds
        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "timeout"
        :returns: (dict) A dict of metric data received in response of the query sent
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code
        """
        start = round(start_time.timestamp())
        end = round(end_time.timestamp())
        params = params or {}
        data = None
        query = str(query)
        # using the query_range API to get raw data
        response = self._session.get(
            "{0}/api/v1/query_range".format(self.url),
            params={**{"query": query, "start": start, "end": end, "step": step}, **params},
            verify=self.ssl_verification,
            headers=self.headers,
        )
        if response.status_code == 200:
            data = response.json()["data"]["result"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )
        return data

    def get_metric_aggregation(
        self,
        query: str,
        operations: list,
        start_time: datetime = None,
        end_time: datetime = None,
        step: str = "15",
        params: dict = None,
    ):
        """
        Get aggregations on metric values received from PromQL query.

        This method takes as input a string which will be sent as a query to
        the specified Prometheus Host. This query is a PromQL query. And, a
        list of operations to perform such as- sum, max, min, deviation, etc.
        with start_time, end_time and step.

        The received query is passed to the custom_query_range method which returns
        the result of the query and the values are extracted from the result.

        :param query: (str) This is a PromQL query, a few examples can be found
          at https://prometheus.io/docs/prometheus/latest/querying/examples/
        :param operations: (list) A list of operations to perform on the values.
          Operations are specified in string type.
        :param start_time: (datetime) A datetime object that specifies the query range start time.
        :param end_time: (datetime) A datetime object that specifies the query range end time.
        :param step: (str) Query resolution step width in duration format or float number of seconds
        :param params: (dict) Optional dictionary containing GET parameters to be
          sent along with the API request, such as "timeout"
          Available operations - sum, max, min, variance, nth percentile, deviation
          and average.

        :returns: (dict) A dict of aggregated values received in response to the operations
          performed on the values for the query sent.

        Example output:
          .. code-block:: python

            {
                'sum': 18.05674,
                'max': 6.009373
             }
        """
        if not isinstance(operations, list):
            raise TypeError("Operations can be only of type list")
        if len(operations) == 0:
            _LOGGER.debug("No operations found to perform")
            return None
        aggregated_values = {}
        query_values = []
        if start_time is not None and end_time is not None:
            data = self.custom_query_range(
                query=query, params=params, start_time=start_time, end_time=end_time, step=step
            )
            for result in data:
                values = result["values"]
                for val in values:
                    query_values.append(float(val[1]))
        else:
            data = self.custom_query(query, params)
            for result in data:
                val = float(result["value"][1])
                query_values.append(val)

        if len(query_values) == 0:
            _LOGGER.debug("No values found for given query.")
            return None

        np_array = numpy.array(query_values)
        for operation in operations:
            if operation == "sum":
                aggregated_values["sum"] = numpy.sum(np_array)
            elif operation == "max":
                aggregated_values["max"] = numpy.max(np_array)
            elif operation == "min":
                aggregated_values["min"] = numpy.min(np_array)
            elif operation == "average":
                aggregated_values["average"] = numpy.average(np_array)
            elif operation.startswith("percentile"):
                percentile = float(operation.split("_")[1])
                aggregated_values["percentile_" + str(percentile)] = numpy.percentile(
                    query_values, percentile
                )
            elif operation == "deviation":
                aggregated_values["deviation"] = numpy.std(np_array)
            elif operation == "variance":
                aggregated_values["deviation"] = numpy.var(np_array)
            else:
                raise TypeError("Invalid operation: " + operation)
        return aggregated_values
