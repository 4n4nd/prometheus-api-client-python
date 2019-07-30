import unittest
import json
import os
import datetime
from prometheus_api_client import MetricsList


class TestMetricsList(unittest.TestCase):
    def setUp(self):
        """
        read metrics stored as jsons in './tests/metrics'
        """
        self.raw_metrics_list = list()
        for (dir_path, _, file_names) in os.walk("./tests/metrics"):
            self.raw_metrics_list.extend(
                [json.load(open(os.path.join(dir_path, file))) for file in file_names]
            )

    def test_setup(self):
        """
        Check if setup was done correctly
        """
        self.assertEqual(
            8, len(self.raw_metrics_list), "incorrect number json files read (incorrect test setup)"
        )

    def test_init(self):
        """
        Test if metrics initialized in the list are correct
        """
        self.assertEqual(
            9,  # manually check the number of unique metric time-series
            len(MetricsList(self.raw_metrics_list)),
            "incorrect number of unique metric timeseries",
        )

    def test_init_single_metric(self):
        self.assertEqual(
            1,
            len(MetricsList(self.raw_metrics_list[0][0])),
            "incorrect number of Metric objects initialized for a raw metric not in a list",
        )
        self.assertEqual(
            1,
            len(MetricsList([self.raw_metrics_list[0][0]])),
            "incorrect number of Metric objects initialized for a single metric list",
        )

    def test_unique_metric_combination(self):
        start_time = datetime.datetime(2019, 7, 28, 10, 0)
        start_time_plus_1m = datetime.datetime(2019, 7, 28, 10, 1)
        end_time = datetime.datetime(2019, 7, 30, 10, 0)
        end_time_minus_1m = datetime.datetime(2019, 7, 30, 9, 59)

        self.assertTrue(
            MetricsList(self.raw_metrics_list)[0].start_time > start_time,
            "Combined metric start time incorrect",
        )
        self.assertTrue(
            MetricsList(self.raw_metrics_list)[0].start_time < start_time_plus_1m,
            "Combined metric start time incorrect",
        )
        self.assertTrue(
            MetricsList(self.raw_metrics_list)[0].end_time < end_time,
            "Combined metric end time incorrect",
        )
        self.assertTrue(
            MetricsList(self.raw_metrics_list)[0].end_time > end_time_minus_1m,
            "Combined metric end time incorrect",
        )


if __name__ == "__main__":
    unittest.main()
