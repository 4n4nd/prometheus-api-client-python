import json
import os

class TestWithMetrics:
    class Common(object):
        def loadMetrics(self):
            """
            read metrics stored as jsons in './tests/metrics'
            """
            self.raw_metrics_list = list()
            for (dir_path, _, file_names) in os.walk("./tests/metrics"):
                for file in file_names:
                    with open(os.path.join(dir_path, file)) as json_fd:
                        self.raw_metrics_list.append(json.load(json_fd))

        def test_setup(self):
            """
            Check if setup was done correctly
            """
            self.assertEqual(8, len(self.raw_metrics_list), "incorrect number json files read")
