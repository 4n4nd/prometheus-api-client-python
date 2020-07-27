import unittest
import json
import os
from prometheus_api_client import MetricRangeDataFrame

class TestMetricRangeDataFrame(unittest.TestCase):
    def setUp(self):
        """
        read metrics stored as jsons in './tests/metrics'
        """
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
        """
        Check if setup was done correctly
        """
        self.assertEqual(
            8, len(self.raw_metrics_list), "incorrect number json files read (incorrect test setup)"
        )


    def test_init_shape(self):
        """
        Test if dataframe initialized is of correct shape
        """
        # check shape
        # each metric json contains number of timestamps equal to number entries * number of timestamps in each series 
        # we're assuming each series has the same number of timestamps
        # 3 labels
        for current_metric_list in self.raw_metrics_list:
            df = MetricRangeDataFrame(current_metric_list)
            num_values = sum([len(v["values"]) for v in current_metric_list])
            self.assertEqual(
                (len(df.index.values), 5),    # shape[1] = 4xlabels + value
                (num_values, 5),
                "incorrect dataframe shape",
            )

    def test_init_timestamps(self):
        """
        Test if dataframe contains the correct timestamp indices
        """
        # check that the timestamp indices in each series are the same
        for curr_metric_list in self.raw_metrics_list:
            self.assertEqual(
                set(MetricRangeDataFrame(curr_metric_list).index.values),
                set([v[0] for s in curr_metric_list for v in s["values"] ])
            )


    def test_init_columns(self):
        """
        Test if dataframe initialized has correct columns
        """
        for curr_metric_labels, curr_metric_list in zip(self.raw_metrics_labels, self.raw_metrics_list):
            self.assertEqual(
                curr_metric_labels.union({"value"}),
                set(MetricRangeDataFrame(curr_metric_list).columns),
                "incorrect dataframe columns",
            )


    def test_init_single_metric(self):
        """
        Test if dataframe initialized is of correct shape when
        1. json object is passed as data
        2. list with single json object is passed as data
        """
        # check shape when single json passed
        num_vals = len(self.raw_metrics_list[0][0]["values"])
        self.assertEqual(
            (num_vals, 5),
            MetricRangeDataFrame(self.raw_metrics_list[0][0]).shape,
            "incorrect dataframe shape when initialized with json",
        )
        # check shape when list with single json passed
        self.assertEqual(
            (num_vals, 5),
            MetricRangeDataFrame([self.raw_metrics_list[0][0]]).shape,
            "incorrect dataframe shape when initialized with single json list",
        )


if __name__ == "__main__":
    unittest.main()
