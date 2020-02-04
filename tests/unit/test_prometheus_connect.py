from datetime import datetime, timedelta

import pytest
import requests

from prometheus_api_client.prometheus_connect import PrometheusConnect
from prometheus_api_client.exceptions import PrometheusApiClientException

from .prom_responses import ALL_METRICS


def test_network_blocked():
    """
    For documenting purposes, keep in mind that all network interactions blocked in this module
    """
    resp = requests.get("http://some-url-there.org")
    assert resp.content == b"BOOM!"
    assert resp.status_code == 403


class TestPrometheusConnect:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.pc = PrometheusConnect(url="http://mocked-host.org")

    def test_unauthorized(self, mocked_response):
        with mocked_response("Unauthorized", status_code=403):
            with pytest.raises(PrometheusApiClientException) as exc:
                self.pc.all_metrics()
        assert "HTTP Status Code 403 (b'Unauthorized')" in str(exc)

    def test_broken_responses(self):
        with pytest.raises(PrometheusApiClientException) as exc:
            self.pc.all_metrics()
        assert "HTTP Status Code 403 (b'BOOM!')" in str(exc)

        with pytest.raises(PrometheusApiClientException) as exc:
            self.pc.get_current_metric_value("metric")
        assert "HTTP Status Code 403 (b'BOOM!')" in str(exc)

        with pytest.raises(PrometheusApiClientException) as exc:
            self.pc.get_metric_range_data("metric")
        assert "HTTP Status Code 403 (b'BOOM!')" in str(exc)

        with pytest.raises(PrometheusApiClientException) as exc:
            self.pc.custom_query_range("query", datetime.now(), datetime.now(), "1")
        assert "HTTP Status Code 403 (b'BOOM!')" in str(exc)

        with pytest.raises(PrometheusApiClientException) as exc:
            self.pc.custom_query("query")
        assert "HTTP Status Code 403 (b'BOOM!')" in str(exc)

    def test_all_metrics(self, mocked_response):
        with mocked_response(ALL_METRICS) as handler:
            assert len(self.pc.all_metrics())
            assert handler.call_count == 1
            request = handler.requests[0]
            assert request.path_url == "/api/v1/label/__name__/values"

    def test_get_metric_range_data_with_incorrect_input_types(self):
        start_time = datetime.now() - timedelta(minutes=20)
        chunk_size = timedelta(minutes=7)
        end_time = datetime.now() - timedelta(minutes=10)

        with pytest.raises(TypeError):
            self.pc.get_metric_range_data(
                metric_name="up", start_time="20m", end_time=end_time, chunk_size=chunk_size
            )
        with pytest.raises(TypeError):
            self.pc.get_metric_range_data(
                metric_name="up", start_time=start_time, end_time="10m", chunk_size=chunk_size
            )
        with pytest.raises(TypeError):
            self.pc.get_metric_range_data(
                metric_name="up", start_time=start_time, end_time=end_time, chunk_size="10m"
            )
