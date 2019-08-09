"""
A Class for collection of metrics from a Prometheus Host.
"""
from urllib.parse import urlparse
import bz2
import os
import sys
import json
import logging
from datetime import datetime, timedelta
import requests
from retrying import retry

# set up logging
_LOGGER = logging.getLogger(__name__)

# In case of a connection failure try 2 more times
MAX_REQUEST_RETRIES = 3
# wait 1 second before retrying in case of an error
CONNECTION_RETRY_WAIT_TIME = 1000


class PrometheusConnect:
    """
    A Class for collection of metrics from a Prometheus Host

    :param url: (str) url for the prometheus host
    :param headers: (dict) A dictionary of http headers to be used to communicate with
        the host. Example: {"Authorization": "bearer my_oauth_token_to_the_host"}
    :param disable_ssl: (bool) If set to True, will disable ssl certificate verification
        for the http requests made to the prometheus host
    """

    def __init__(
        self, url: str = "http://127.0.0.1:9090", headers: dict = None, disable_ssl: bool = False
    ):
        """
        Constructor for the class PrometheusConnect
        """
        self.headers = headers
        self.url = url
        self.prometheus_host = urlparse(self.url).netloc
        self._all_metrics = None
        self.ssl_verification = not disable_ssl

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def all_metrics(self, params: dict = None):
        """
        Get the list of all the metrics that the prometheus host scrapes

        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :returns: (list) A list of names of all the metrics available from the
            specified prometheus host
        :raises: (Http Response error) Raises an exception in case of a connection error
        """
        params = params or {}
        response = requests.get(
            "{0}/api/v1/label/__name__/values".format(self.url),
            verify=self.ssl_verification,
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            self._all_metrics = response.json()["data"]
        else:
            raise Exception(
                "HTTP Status Code {} ({})".format(response.status_code, response.content)
            )
        return self._all_metrics

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def get_current_metric_value(
        self, metric_name: str, label_config: dict = None, params: dict = None
    ):
        """
        A method to get the current metric value for the specified metric
        and label configuration.

        :param metric_name: (str) The name of the metric
        :param label_config: (dict) A dictionary that specifies metric labels and their
            values
        :param params: (dict) Optional dictionary containing GET parameters to be sent
            along with the API request, such as "time"
        :returns: (list) A list of current metric values for the specified metric
        :raises: (Http Response error) Raises an exception in case of a connection error

        Example Usage:
            ``prom = PrometheusConnect()``

            ``my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}``

            ``prom.get_current_metric_value(metric_name='up', label_config=my_label_config)``
        """
        params = params or {}
        data = []
        if label_config:
            label_list = [str(key + "=" + "'" + label_config[key] + "'") for key in label_config]
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        # using the query API to get raw data
        response = requests.get(
            "{0}/api/v1/query".format(self.url),
            params={**{"query": query}, **params},
            verify=self.ssl_verification,
            headers=self.headers,
        )

        if response.status_code == 200:
            data += response.json()["data"]["result"]
        else:
            raise Exception(
                "HTTP Status Code {} ({})".format(response.status_code, response.content)
            )
        return data

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
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
        """
        A method to get the current metric value for the specified metric
        and label configuration.

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
        :raises: (Exception) Raises an exception in case of a connection error
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

        if (end_time - start_time).total_seconds() < chunk_size.total_seconds():
            sys.exit("specified chunk_size is too big")
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
            response = requests.get(
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
                raise Exception(
                    "HTTP Status Code {} ({})".format(response.status_code, response.content)
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
        """
        Store metrics on the local filesystem, optionally  with bz2 compression

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
        """
        Adds a timestamp to the filename before it is stored

        :param metric_name: (str) the name of the metric being saved
        :param end_timestamp: (int) timestamp in any format understood by \
            datetime.datetime.fromtimestamp()
        :returns: (str) the generated path
        """
        end_timestamp = datetime.fromtimestamp(end_timestamp)
        directory_name = end_timestamp.strftime("%Y%m%d")
        timestamp = end_timestamp.strftime("%Y%m%d%H%M")
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

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def custom_query(self, query: str, params: dict = None):
        """
        A method to send a custom query to a Prometheus Host.

        This method takes as input a string which will be sent as a query to
        the specified Prometheus Host. This query is a PromQL query.

        :param query: (str) This is a PromQL query, a few examples can be found
            at https://prometheus.io/docs/prometheus/latest/querying/examples/
        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :returns: (list) A list of metric data received in response of the query sent
        :raises: (Exception) Raises an exception in case of a connection error
        """
        params = params or {}
        data = None
        query = str(query)
        # using the query API to get raw data
        response = requests.get(
            "{0}/api/v1/query".format(self.url),
            params={**{"query": query}, **params},
            verify=self.ssl_verification,
            headers=self.headers,
        )
        if response.status_code == 200:
            data = response.json()["data"]["result"]
        else:
            raise Exception(
                "HTTP Status Code {} ({})".format(response.status_code, response.content)
            )

        return data
