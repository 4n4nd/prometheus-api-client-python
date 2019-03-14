from urllib.parse import urlparse
import requests
import datetime
import json
import time
import dateparser
import sys
import os
from retrying import retry
import bz2

# set up logging
import logging
_LOGGER = logging.getLogger(__name__)

# Disable SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DEBUG = False
MAX_REQUEST_RETRIES = 3
CONNECTION_RETRY_WAIT_TIME = 1000 # wait 1 second before retrying in case of an error

class PrometheusConnect:
    """docstring for Prometheus."""
    def __init__(self, url='127.0.0.1:9090', token=None):
        self.headers = { 'Authorization': "bearer {}".format(token) }
        self.url = url
        self.prometheus_host = urlparse(self.url).netloc
        self._all_metrics = None

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def all_metrics(self):
        '''
        Get the list of all the metrics that the prometheus host has
        '''
        response = requests.get('{0}/api/v1/label/__name__/values'.format(self.url),
                                verify=False, # Disable ssl certificate verification temporarily
                                headers=self.headers)

        if response.status_code == 200:
            self._all_metrics = response.json()['data']
        else:
            raise Exception("HTTP Status Code {} {} ({})".format(
                response.status_code,
                requests.status_codes._codes[response.status_code][0],
                response.content
            ))
        return self._all_metrics

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def get_current_metric_value(self, metric_name, label_config = None):
        data = []
        if label_config:
            label_list = [str(key+"="+ "'" + label_config[key]+ "'") for key in label_config]
            # print(label_list)
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        response = requests.get('{0}/api/v1/query'.format(self.url),    # using the query API to get raw data
                                params={'query': query},#label_config},
                                verify=False, # Disable ssl certificate verification temporarily
                                headers=self.headers)

        if response.status_code == 200:
            data += response.json()['data']['result']
        else:
            raise Exception("HTTP Status Code {} {} ({})".format(
                response.status_code,
                requests.status_codes._codes[response.status_code][0],
                response.content
            ))
        return (data)

    @retry(stop_max_attempt_number=MAX_REQUEST_RETRIES, wait_fixed=CONNECTION_RETRY_WAIT_TIME)
    def get_metric_range_data(self, metric_name, start_time, end_time='now', chunk_size=None,label_config=None, store_locally=False):
        data = []

        start = int(dateparser.parse(str(start_time)).timestamp())
        end = int(dateparser.parse(str(end_time)).timestamp())

        if not chunk_size:
            chunk_seconds = int(end - start)
            chunk_size = str(int(chunk_seconds)) + "s"
        else:
            chunk_seconds = int(round((dateparser.parse('now') - dateparser.parse(chunk_size)).total_seconds()))

        if int(end-start) < chunk_seconds:
            sys.exit("specified chunk_size is too big")

        if label_config:
            label_list = [str(key+"="+ "'" + label_config[key]+ "'") for key in label_config]
            # print(label_list)
            query = metric_name + "{" + ",".join(label_list) + "}"
        else:
            query = metric_name

        while start < end:
            # print(chunk_size)
            response = requests.get('{0}/api/v1/query'.format(self.url),    # using the query API to get raw data
                                params={'query': query + '[' + chunk_size + ']',
                                        'time': start + chunk_seconds
                                        },
                                verify=False, # Disable ssl certificate verification temporarily
                                headers=self.headers)
            if response.status_code == 200:
                data += response.json()['data']['result']
            else:
                raise Exception("HTTP Status Code {} {} ({})".format(
                    response.status_code,
                    requests.status_codes._codes[response.status_code][0],
                    response.content
                ))
            if store_locally:
                # store it locally
                self.store_metric_values_local(metric_name , (response.json()['data']['result']), start + chunk_seconds)

            start += chunk_seconds
        return (data)

    def store_metric_values_local(self, metric_name, values, end_timestamp, file_path=None, compressed=True):
        '''
        Function to store metrics locally
        '''
        if not values:
            return "No values for {}".format(metric_name)

        if not file_path:
            file_path = self._metric_filename(metric_name, end_timestamp)

        if compressed:
            payload = bz2.compress(str(values).encode('utf-8'))
            file_path = file_path + ".bz2"
        else:
            payload = (str(values).encode('utf-8'))

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(payload)

    def _metric_filename(self, metric_name, end_timestamp):
        '''
        Adds a timestamp to the filename before it is stored
        '''
        end_timestamp = dateparser.parse(str(end_timestamp))
        directory_name = end_timestamp.strftime("%Y%m%d")
        timestamp = end_timestamp.strftime("%Y%m%d%H%M")
        object_path = "./metrics/" + self.prometheus_host + "/" + metric_name + "/" + directory_name + "/" + timestamp + ".json"
        return object_path

    def pretty_print_metric(self, metric_data):
        data = metric_data
        for metric in data:
            print(json.dumps(metric, indent=4, sort_keys=True))
