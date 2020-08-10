"""Unit tests for Metrics Class."""
import unittest
import datetime
from prometheus_api_client import Metric
from .test_with_metrics import TestWithMetrics


class TestMetric(unittest.TestCase, TestWithMetrics.Common):
    """unit tests for Metrics Class."""

    def setUp(self):
        """Load metrics stored as jsons."""
        self.load_metrics()

    def test_init(self):  # noqa D102
        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertEqual("up", test_metric_object.metric_name, "incorrect metric name")

    def test_metric_start_time(self):  # noqa D102
        start_time = datetime.datetime(2019, 7, 28, 10, 0)
        start_time_plus_1m = datetime.datetime(2019, 7, 28, 10, 1)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertTrue(test_metric_object.start_time > start_time, "incorrect metric start time")
        self.assertTrue(
            test_metric_object.start_time < start_time_plus_1m, "incorrect metric start time"
        )

    def test_metric_end_time(self):  # noqa D102
        end_time = datetime.datetime(2019, 7, 28, 16, 00)
        end_time_minus_1m = datetime.datetime(2019, 7, 28, 15, 59)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        self.assertTrue(
            test_metric_object.end_time > end_time_minus_1m, "incorrect metric end time"
        )
        self.assertTrue(test_metric_object.end_time < end_time, "incorrect metric end time")

    def test_metric_equality(self):  # noqa D102
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

    def test_metric_addition(self):  # noqa D102
        with self.assertRaises(TypeError, msg="incorrect addition of two metrics"):
            _ = Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[0][1])

        sum_metric = Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[1][0])
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

    def test_oldest_data_datetime_with_datetime(self):  # noqa D102
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

    def test_oldest_data_datetime_with_timedelta(self):  # noqa D102
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
