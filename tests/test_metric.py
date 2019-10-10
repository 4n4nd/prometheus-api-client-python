"""unit tests for Metrics Class."""
import unittest
import json
import os
import datetime
from prometheus_api_client import Metric


class TestMetric(unittest.TestCase):
    """unit tests for Metrics Class."""

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
        self.assertEqual(8, len(self.raw_metrics_list), "incorrect number json files read")

    def test_init(self):
        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertEqual("up", test_metric_object.metric_name, "incorrect metric name")

    def test_metric_start_time(self):
        start_time = datetime.datetime(2019, 7, 28, 10, 0)
        start_time_plus_1m = datetime.datetime(2019, 7, 28, 10, 1)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertTrue(test_metric_object.start_time > start_time, "incorrect metric start time")
        self.assertTrue(
            test_metric_object.start_time < start_time_plus_1m, "incorrect metric start time"
        )

    def test_metric_end_time(self):
        end_time = datetime.datetime(2019, 7, 28, 16, 00)
        end_time_minus_1m = datetime.datetime(2019, 7, 28, 15, 59)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertTrue(
            test_metric_object.end_time > end_time_minus_1m, "incorrect metric end time"
        )
        self.assertTrue(test_metric_object.end_time < end_time, "incorrect metric end time")

    def test_metric_equality(self):
        self.assertEqual(
            Metric(self.raw_metrics_list[0][0]),
            Metric(self.raw_metrics_list[1][0]),
            "incorrect inequality",
        )
        self.assertNotEqual(
            Metric(self.raw_metrics_list[0][0]),
            Metric(self.raw_metrics_list[0][1]),
            "incorrect equality",
        )

    def test_metric_addition(self):
        with self.assertRaises(TypeError, msg="incorrect addition of two metrics"):
            _ = Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[0][1])

        sum_metric = Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[1][0])
        print(sum_metric)
        self.assertIsInstance(sum_metric, Metric, msg="The sum is not a Metric")
        self.assertEqual(
            sum_metric.start_time,
            Metric(self.raw_metrics_list[0][0]).start_time,
            "Incorrect Start time after addition",
        )
        self.assertEqual(
            sum_metric.end_time,
            Metric(self.raw_metrics_list[1][0]).end_time,
            "Incorrect End time after addition",
        )

    def test_oldest_data_datetime_with_datetime(self):
        with self.assertRaises(TypeError, msg="incorrect parameter type accepted"):
            _ = Metric(self.raw_metrics_list[0][0], oldest_data_datetime="2d")

        expected_start_time = Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        new_metric = Metric(
            self.raw_metrics_list[0][0], oldest_data_datetime=expected_start_time
        ) + Metric(self.raw_metrics_list[1][0])

        self.assertEqual(
            expected_start_time, new_metric.start_time, "Incorrect Start time after addition"
        )
        self.assertEqual(
            expected_start_time,
            new_metric.metric_values.iloc[0, 0],
            "Incorrect Start time after addition (in df)",
        )

    def test_oldest_data_datetime_with_timedelta(self):
        expected_start_time = Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        time_delta = (
            Metric(self.raw_metrics_list[1][0]).metric_values.iloc[-1, 0]
            - Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        )
        new_metric = Metric(self.raw_metrics_list[0][0], oldest_data_datetime=time_delta) + Metric(
            self.raw_metrics_list[1][0]
        )
        self.assertEqual(
            expected_start_time, new_metric.start_time, "Incorrect Start time after addition"
        )


if __name__ == "__main__":
    unittest.main()
