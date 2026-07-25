"""Test module for class PrometheusConnect."""
import unittest

from prometheus_api_client.metric_query import query_to_str

class TestMetricQuery(unittest.TestCase):
    """Test module for metric query."""

    def test_query_to_str_with_wrong_label_query(self):  # noqa D102
        # wrong op ('~=' instead of '=~')
        with self.assertRaises(ValueError, msg=f"unknown label operator: '~='"):
            _ = query_to_str(
                metric_name="up",
                label_query={"some_label": ("~=", "some-value-.*")}
            )
        # inverted label value and op
        with self.assertRaises(ValueError, msg=f"unknown label operator: 'some-value-.*'"):
            _ = query_to_str(
                metric_name="up",
                label_query={"some_label": ("some-value-.*", "=~")}
            )
        # Wrong number of label query arguments
        with self.assertRaises(ValueError, msg=f"wrong number of elements in label query with operator: 3 instead of 2"):
            _ = query_to_str(
                metric_name="up",
                label_query={"some_label": ("=~", "some-value-.*", "whatever")}
            )
    def test_query_to_str_with_correct_label_query(self):  # noqa D102
        correct_label_queries = [
            { "some_label": "some-value"}, # exact match
            { "some_label": ("=", "some-value")}, # exact match, explicit op
            { "some_label": ("!=", "some-value")}, # negative match
            { "some_label": ("=~", "some-value-.*")}, # regex match
            { "some_label": ("!~", "some-value-.*")}, # negative regex match
        ]
        for label_query in correct_label_queries:
            try:
                _ = query_to_str(
                    metric_name="up",
                    label_query=label_query
                )
            except Exception as e:
                self.fail(f"query_to_str('up') with label_config raised an unexpected exception: {e}")


if __name__ == "__main__":
    unittest.main()