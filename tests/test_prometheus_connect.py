"""Test module for class PrometheusConnect."""
import unittest
import os
from datetime import datetime, timedelta

import requests
from requests.packages.urllib3.util.retry import Retry

from prometheus_api_client import MetricsList, PrometheusConnect, PrometheusApiClientException

from .mocked_network import BaseMockedNetworkTestcase


class TestPrometheusConnect(unittest.TestCase):
    """Test module for class PrometheusConnect."""

    def setUp(self):
        """Set up connection settings for prometheus."""
        self.prometheus_host = os.getenv("PROM_URL")
        self.pc = PrometheusConnect(url=self.prometheus_host, disable_ssl=True)

    def test_metrics_list(self):
        """Check if setup was done correctly."""
        metrics_list = self.pc.all_metrics()
        self.assertTrue(len(metrics_list) > 0, "no metrics received from prometheus")

    def test_get_metric_range_data(self):  # noqa D102
        start_time = datetime.now() - timedelta(minutes=10)
        end_time = datetime.now()
        metric_data = self.pc.get_metric_range_data(
            metric_name="up", start_time=start_time, end_time=end_time
        )

        metric_objects_list = MetricsList(metric_data)

        self.assertTrue(len(metric_objects_list) > 0, "no metrics received from prometheus")
        self.assertTrue(
            start_time.timestamp() < metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time",
        )
        self.assertTrue(
            (start_time + timedelta(minutes=1)).timestamp()
            > metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time",
        )
        self.assertTrue(
            end_time.timestamp() > metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time",
        )
        self.assertTrue(
            (end_time - timedelta(minutes=1)).timestamp()
            < metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time",
        )

    def test_get_metric_range_data_with_chunk_size(self):  # noqa D102
        start_time = datetime.now() - timedelta(minutes=65)
        chunk_size = timedelta(minutes=7)
        end_time = datetime.now() - timedelta(minutes=5)
        metric_data = self.pc.get_metric_range_data(
            metric_name="up", start_time=start_time, end_time=end_time, chunk_size=chunk_size
        )

        metric_objects_list = MetricsList(metric_data)

        self.assertTrue(len(metric_objects_list) > 0, "no metrics received from prometheus")
        self.assertTrue(
            start_time.timestamp() < metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time (with given chunk_size)",
        )
        self.assertTrue(
            (start_time + timedelta(minutes=1)).timestamp()
            > metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time (with given chunk_size)",
        )
        self.assertTrue(
            end_time.timestamp() > metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time (with given chunk_size)",
        )
        self.assertTrue(
            (end_time - timedelta(minutes=1)).timestamp()
            < metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time (with given chunk_size)",
        )

    def test_get_metric_range_data_with_incorrect_input_types(self):  # noqa D102
        start_time = datetime.now() - timedelta(minutes=20)
        chunk_size = timedelta(minutes=7)
        end_time = datetime.now() - timedelta(minutes=10)

        with self.assertRaises(ValueError, msg="specified chunk_size is too big"):
            _ = self.pc.get_metric_range_data(
                metric_name="up",
                start_time=start_time,
                end_time=end_time,
                chunk_size=timedelta(minutes=30),
            )
        with self.assertRaises(TypeError, msg="start_time accepted invalid value type"):
            _ = self.pc.get_metric_range_data(
                metric_name="up", start_time="20m", end_time=end_time, chunk_size=chunk_size
            )
        with self.assertRaises(TypeError, msg="end_time accepted invalid value type"):
            _ = self.pc.get_metric_range_data(
                metric_name="up", start_time=start_time, end_time="10m", chunk_size=chunk_size
            )
        with self.assertRaises(TypeError, msg="chunk_size accepted invalid value type"):
            _ = self.pc.get_metric_range_data(
                metric_name="up", start_time=start_time, end_time=end_time, chunk_size="10m"
            )

    def test_get_metric_aggregation(self):  # noqa D102
        operations = ["sum", "max", "min", "variance", "percentile_50", "deviation", "average"]
        start_time = datetime.now() - timedelta(minutes=10)
        end_time = datetime.now()
        step = "15"
        aggregated_values = self.pc.get_metric_aggregation(
            query="up", operations=operations, start_time=start_time, end_time=end_time, step=step
        )

        self.assertTrue(len(aggregated_values) > 0, "no values received after aggregating")

    def test_get_metric_aggregation_with_incorrect_input_types(self):  # noqa D102
        with self.assertRaises(TypeError, msg="operations accepted invalid value type"):
            _ = self.pc.get_metric_aggregation(query="up", operations="sum")

    def test_retry_on_error(self):  # noqa D102
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[400])
        pc = PrometheusConnect(url=self.prometheus_host, disable_ssl=True, retry=retry)

        with self.assertRaises(requests.exceptions.RetryError, msg="too many 400 error responses"):
            pc.custom_query("BOOM.BOOM!#$%")


class TestPrometheusConnectWithMockedNetwork(BaseMockedNetworkTestcase):
    """Network is blocked in this testcase, see base class."""

    def setUp(self):  # noqa D102
        self.pc = PrometheusConnect(url="http://doesnt_matter.xyz", disable_ssl=True)

    def test_network_is_blocked(self):  # noqa D102
        resp = requests.get("https://google.com")
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.text, "BOOM!")

    def test_how_mock_prop_works(self):  # noqa D102
        with self.mock_response("kekekeke", status_code=500) as handler:
            self.assertEqual(len(handler.requests), 0)
            resp = requests.get("https://redhat.com")
            self.assertEqual(resp.status_code, 500)
            self.assertEqual(resp.text, "kekekeke")

            self.assertEqual(len(handler.requests), 1)
            request = handler.requests[0]
            self.assertEqual(request.url, "https://redhat.com/")

    def test_unauthorized(self):  # noqa D102
        with self.mock_response("Unauthorized", status_code=403):
            with self.assertRaises(PrometheusApiClientException) as exc:
                self.pc.all_metrics()
        self.assertEqual("HTTP Status Code 403 (b'Unauthorized')", str(exc.exception))

    def test_broken_responses(self):  # noqa D102
        with self.assertRaises(PrometheusApiClientException) as exc:
            self.pc.all_metrics()
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

        with self.assertRaises(PrometheusApiClientException) as exc:
            self.pc.get_current_metric_value("metric")
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

        with self.assertRaises(PrometheusApiClientException) as exc:
            self.pc.get_metric_range_data("metric")
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

        with self.assertRaises(PrometheusApiClientException) as exc:
            self.pc.custom_query_range("query", datetime.now(), datetime.now(), "1")
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

        with self.assertRaises(PrometheusApiClientException) as exc:
            self.pc.custom_query("query")
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

        with self.assertRaises(PrometheusApiClientException) as exc:
            start_time = datetime.now() - timedelta(minutes=10)
            end_time = datetime.now()
            self.pc.get_metric_aggregation(
                "query", ["sum", "deviation"], start_time, end_time, "15"
            )
        self.assertEqual("HTTP Status Code 403 (b'BOOM!')", str(exc.exception))

    def test_all_metrics_method(self):  # noqa D102
        all_metrics_payload = {"status": "success", "data": ["up", "alerts"]}

        with self.mock_response(all_metrics_payload) as handler:
            self.assertTrue(len(self.pc.all_metrics()))
            self.assertEqual(handler.call_count, 1)
            request = handler.requests[0]
            self.assertEqual(request.path_url, "/api/v1/label/__name__/values")
