"""Unit Tests for MetricSnapshotDataFrame."""
import unittest
import json
import os

import pytest

from prometheus_api_client import MetricSnapshotDataFrame
from prometheus_api_client.exceptions import MetricValueConversionError
from pandas.api.types import is_datetime64_any_dtype as is_dtype_datetime


class TestMetricSnapshotDataFrame(unittest.TestCase):  # noqa D101
    def setUp(self):
        """Read metrics stored as jsons in './tests/metrics'."""
        self.raw_metrics_list = list()
        self.raw_metrics_labels = list()
        for (dir_path, _, file_names) in os.walk("./tests/metrics"):
            for fname in file_names:
                with open(os.path.join(dir_path, fname), "rb") as f:
                    metric_jsons = json.load(f)

                # save json list
                self.raw_metrics_list.extend([metric_jsons])

                # save label configs
                labels = set()
                for i in metric_jsons:
                    labels.update(set(i["metric"].keys()))
                self.raw_metrics_labels.append(labels)

    def test_setup(self):
        """Check if setup was done correctly."""
        self.assertEqual(
            8, len(self.raw_metrics_list), "incorrect number json files read (incorrect test setup)"
        )

    def test_init_shape(self):
        """Test if dataframe initialized is of correct shape."""
        # check shape
        # each json file contains 9 entries, 4 labels
        for current_metric_list in self.raw_metrics_list:
            self.assertEqual(
                (9, 6),  # shape[1] = 4xlabels + timestamp + value
                MetricSnapshotDataFrame(current_metric_list).shape,
                "incorrect dataframe shape",
            )

    def test_init_columns(self):
        """Test if dataframe initialized has correct columns."""
        for curr_metric_labels, curr_metric_list in zip(
            self.raw_metrics_labels, self.raw_metrics_list
        ):
            self.assertEqual(
                curr_metric_labels.union({"timestamp", "value"}),
                set(MetricSnapshotDataFrame(curr_metric_list).columns),
                "incorrect dataframe columns",
            )

    def test_timestamp_dtype_conversion(self):
        """Test if the timestamp in the dataframe initialized has correct dtype."""
        for curr_metric_list in self.raw_metrics_list:
            # timestamp column should be datetime type by default
            curr_df = MetricSnapshotDataFrame(curr_metric_list,)
            self.assertTrue(
                is_dtype_datetime(curr_df["timestamp"]),
                "incorrect dtype for timestamp column (expected datetime dtype)",
            )

            # if explicitly set to false, conversion to dt shouldnt take place
            curr_df = MetricSnapshotDataFrame(curr_metric_list, ts_as_datetime=False,)
            self.assertFalse(
                is_dtype_datetime(curr_df["timestamp"]),
                "incorrect dtype for timestamp column (expected non-datetime dtype)",
            )

    def test_init_single_metric(self):
        """
        Test if dataframe initialized is of correct shape.

        1. json object is passed as data
        2. list with single json object is passed as data
        """
        # check shape when single json passed
        self.assertEqual(
            (1, 6),
            MetricSnapshotDataFrame(self.raw_metrics_list[0][0]).shape,
            "incorrect dataframe shape when initialized with json",
        )
        # check shape when list with single json passed
        self.assertEqual(
            (1, 6),
            MetricSnapshotDataFrame([self.raw_metrics_list[0][0]]).shape,
            "incorrect dataframe shape when initialized with single json list",
        )

    def test_init_multiple_metrics(self):
        """Ensures metric values provided as strings are properly cast to a numeric value (in this case, a float)."""
        raw_data = [
            {"metric": {"fake": "data",}, "value": [1627485628.789, "26.82068965517243"],},
            {"metric": {"fake": "data",}, "value": [1627485628.789, "26.82068965517243"],},
        ]

        test_df = MetricSnapshotDataFrame(data=raw_data)

        self.assertTrue(isinstance(test_df["value"][0], float))

    def test_init_invalid_float_error(self):
        """Ensures metric values provided as strings are properly cast to a numeric value (in this case, a float)."""
        raw_data = [
            {
                "metric": {"fake": "data",},
                "value": [1627485628.789, "26.8206896551724326.82068965517243"],
            },
        ]

        with pytest.raises(MetricValueConversionError):
            MetricSnapshotDataFrame(data=raw_data)


if __name__ == "__main__":
    unittest.main()
