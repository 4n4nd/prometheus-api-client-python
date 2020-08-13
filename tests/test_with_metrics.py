"""Common functions used for Metrics Class."""

import json
import os


class TestWithMetrics:  # noqa D101
    class Common(object):  # noqa D106
        def load_metrics(self):
            """Read metrics stored as jsons in './tests/metrics'."""
            self.raw_metrics_list = list()
            self.raw_metrics_labels = list()
            files = list()

            for (dir_path, _, file_names) in os.walk("./tests/metrics"):
                files.extend([(os.path.join(dir_path, f_name)) for f_name in file_names])

            # Files with metrics need to be loaded in order by timestamp in their names.
            # Several tests depend on order of these files.
            for file_path in sorted(files):
                with open(file_path) as json_fd:
                    metric_jsons = json.load(json_fd)
                    self.raw_metrics_list.append(metric_jsons)

                    # save label configs
                    labels = set()
                    for i in metric_jsons:
                        labels.update(set(i["metric"].keys()))
                    self.raw_metrics_labels.append(labels)

        def test_setup(self):
            """Check if setup was done correctly."""
            self.assertEqual(8, len(self.raw_metrics_list), "incorrect number json files read")
