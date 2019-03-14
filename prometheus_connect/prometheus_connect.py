from urllib.parse import urlparse
import requests
import datetime
import json
import time
import dateparser
import sys
from retrying import retry

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
    def get_metric_range_data(self, metric_name, start_time, end_time='now', chunk_size=None,label_config=None):
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
            start += chunk_seconds
        return (data)
