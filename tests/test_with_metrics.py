import json
import os

class TestWithMetrics:
    class Common(object):
        def loadMetrics(self):
            """
            read metrics stored as jsons in './tests/metrics'
            """
            self.raw_metrics_list = list()
            files = list()

            for (dir_path, _, file_names) in os.walk("./tests/metrics"):
                files.extend([(os.path.join(dir_path, f_name)) for f_name in file_names])

            # Files with metrics need to be loaded in order by timestamp in their names.
            # Several tests depend on order of these files.
            for file_path in sorted(files):
                with open(file_path) as json_fd:
                    self.raw_metrics_list.append(json.load(json_fd))

        def test_setup(self):
            """
            Check if setup was done correctly
            """
            self.assertEqual(8, len(self.raw_metrics_list), "incorrect number json files read")
