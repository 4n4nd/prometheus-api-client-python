"""
Test module for class PrometheusConnect
"""
import unittest
import os
from datetime import datetime, timedelta
from prometheus_api_client import MetricsList, PrometheusConnect


class TestPrometheusConnect(unittest.TestCase):
    """
    Test module for class PrometheusConnect
    """

    def setUp(self):
        """
        set up connection settings for prometheus
        """
        self.prometheus_host = os.getenv("PROM_URL")
        self.pc = PrometheusConnect(url=self.prometheus_host, disable_ssl=True)

    def test_metrics_list(self):
        """
        Check if setup was done correctly
        """
        metrics_list = self.pc.all_metrics()
        self.assertTrue(len(metrics_list) > 0, "no metrics received from prometheus")

    def test_get_metric_range_data(self):
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

    def test_get_metric_range_data_with_chunk_size(self):
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

    def test_get_metric_range_data_with_incorrect_input_types(self):
        start_time = datetime.now() - timedelta(minutes=20)
        chunk_size = timedelta(minutes=7)
        end_time = datetime.now() - timedelta(minutes=10)

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
