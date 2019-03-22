"""
A Class for collection of metrics from a Prometheus Host.
"""
from urllib.parse import urlparse
import bz2
import os
import sys
import json
import logging
import requests
import dateparser
from retrying import retry

# set up logging
_LOGGER = logging.getLogger(__name__)

# In case of a connection failure try 2 more times
MAX_REQUEST_RETRIES = 3
CONNECTION_RETRY_WAIT_TIME = 1000 # wait 1 second before retrying in case of an error

class PrometheusConnect:
    """
    A Class for collection of metrics from a Prometheus Host

    :param url: (str) url for the prometheus host
    :param headers: (dict) A dictionary of http headers to be used to communicate with the host.
                    Example: {"Authorization": "bearer my_oauth_token_to_the_host"}
    :param disable_ssl: (bool) If set to True, will disable ssl certificate verification
                               for the http requests made to the prometheus host

    """
    def __init__(self, url='http://127.0.0.1:9090', headers=None, disable_ssl=False):
        """
        Constructor for the class PrometheusConnect

        """
        self.headers = headers
        self.url = url
        self.prometheus_host = urlparse(self.url).netloc
        self._all_metrics = None
        self.ssl_verification = (not disable_ssl)

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def all_metrics(self):
        """
        Get the list of all the metrics that the prometheus host scrapes

        :return: (list) A list of names of all the metrics available from the
                  specified prometheus host

        :raises: (Http Response error) Raises an exception in case of a connection error

        """
        response = requests.get('{0}/api/v1/label/__name__/values'.format(self.url),
                                verify=self.ssl_verification,
                                headers=self.headers)

        if response.status_code == 200:
            self._all_metrics = response.json()['data']
        else:
            raise Exception("HTTP Status Code {} ({})".format(
                response.status_code,
                response.content
            ))
        return self._all_metrics

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def get_current_metric_value(self, metric_name, label_config=None):
        """
        A method to get the current metric value for the specified metric
        and label configuration.

        :param metric_name: (str) The name of the metric

        :param label_config: (dict) A dictionary that specifies metric labels and their values

        :return: (list) A list of current metric values for the specified metric

        :raises: (Http Response error) Raises an exception in case of a connection error

        Example Usage:
            ``prom = PrometheusConnect()``

            ``my_label_config = {'cluster': 'my_cluster_id', 'label_2': 'label_2_value'}``

            ``prom.get_current_metric_value(metric_name='up', label_config=my_label_config)``

        """
        data = []
        if label_config:
            label_list = [str(key+"="+ "'" + label_config[key]+ "'") for key in label_config]
            # print(label_list)
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        # using the query API to get raw data
        response = requests.get('{0}/api/v1/query'.format(self.url),
                                params={'query': query},
                                verify=self.ssl_verification,
                                headers=self.headers)

        if response.status_code == 200:
            data += response.json()['data']['result']
        else:
            raise Exception("HTTP Status Code {} ({})".format(
                response.status_code,
                response.content
            ))
        return data

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def get_metric_range_data(self,
                              metric_name,
                              label_config=None,
                              start_time='10m',
                              end_time='now',
                              chunk_size=None,
                              store_locally=False):
        """
        A method to get the current metric value for the specified metric
        and label configuration.

        :param metric_name: (str) The name of the metric.

        :param label_config: (dict) A dictionary that specifies metric labels and their values.

        :param start_time:  (str) A string that specifies the metric range start time.

        :param end_time: (str) A string that specifies the metric range end time.

        :param chunk_size: (str) Duration of metric data downloaded in one request.
                          example, setting it to '3h' will download 3 hours
                          worth of data in each request made to the prometheus host
        :param store_locally: (bool) If set to True, will store data locally at,
                              `"./metrics/hostname/metric_date/name_time.json.bz2"`

        :return: (list) A list of metric data for the specified metric in the given time range

        :raises: (Http Response error) Raises an exception in case of a connection error

        """

        data = []

        start = int(dateparser.parse(str(start_time)).timestamp())
        end = int(dateparser.parse(str(end_time)).timestamp())

        if not chunk_size:
            chunk_seconds = int(end - start)
            chunk_size = str(int(chunk_seconds)) + "s"
        else:
            chunk_seconds = (int(round((dateparser.parse('now') -
                                        dateparser.parse(chunk_size)
                                       ).total_seconds())))

        if int(end-start) < chunk_seconds:
            sys.exit("specified chunk_size is too big")

        if label_config:
            label_list = [str(key+"="+ "'" + label_config[key]+ "'") for key in label_config]
            # print(label_list)
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        while start < end:
            # using the query API to get raw data
            response = requests.get('{0}/api/v1/query'.format(self.url),
                                    params={'query': query + '[' + chunk_size + ']',
                                            'time': start + chunk_seconds
                                            },
                                    verify=self.ssl_verification,
                                    headers=self.headers)
            if response.status_code == 200:
                data += response.json()['data']['result']
            else:
                raise Exception("HTTP Status Code {} ({})".format(
                    response.status_code,
                    response.content
                ))
            if store_locally:
                # store it locally
                self._store_metric_values_local(metric_name,
                                                json.dumps(response.json()['data']['result']),
                                                start + chunk_seconds)

            start += chunk_seconds
        return data

    def _store_metric_values_local(self, metric_name, values, end_timestamp, compressed=False):
        '''
        Method to store metrics locally

        '''
        if not values:
            _LOGGER.debug("No values for %s", metric_name)
            return None

        file_path = self._metric_filename(metric_name, end_timestamp)

        if compressed:
            payload = bz2.compress(str(values).encode('utf-8'))
            file_path = file_path + ".bz2"
        else:
            payload = (str(values).encode('utf-8'))

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(payload)

        return file_path

    def _metric_filename(self, metric_name, end_timestamp):
        '''
        Adds a timestamp to the filename before it is stored

        '''
        end_timestamp = dateparser.parse(str(end_timestamp))
        directory_name = end_timestamp.strftime("%Y%m%d")
        timestamp = end_timestamp.strftime("%Y%m%d%H%M")
        object_path = "./metrics/" + self.prometheus_host + "/" + \
                        metric_name + "/" + directory_name + "/" + timestamp + ".json"
        return object_path

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def custom_query(self, query: str):
        """
        A method to send a custom query to a Prometheus Host.

        This method takes as input a string which will be sent as a query to
        the specified Prometheus Host. This query is a PromQL query.

        :param query: (str) This is a PromQL query, a few examples can be found
                        at https://prometheus.io/docs/prometheus/latest/querying/examples/

        :Returns: (list) A list of metric data received in response of the query sent

        :raises: (Http Response error) Raises an exception in case of a connection error

        """
        data = None
        query = str(query)
        # using the query API to get raw data
        response = requests.get('{0}/api/v1/query'.format(self.url),
                                params={'query': query
                                        },
                                verify=self.ssl_verification,
                                headers=self.headers)
        if response.status_code == 200:
            data = response.json()['data']['result']
        else:
            raise Exception("HTTP Status Code {} ({})".format(
                response.status_code,
                response.content
            ))

        return data

def pretty_print_metric(metric_data):
    """
    A function to pretty print the metric data downloaded using class PrometheusConnect.

    :param metric_data: (list) This is the metric data list returned from methods
                            get_metric_range_data and get_current_metric_value

    """
    data = metric_data
    for metric in data:
        print(json.dumps(metric, indent=4, sort_keys=True))
