"""Asynchronous client for collecting metrics from a Prometheus host."""

from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse

try:
    import aiohttp
except ImportError as exc:
    raise ImportError(
        "aiohttp is required for AsyncPrometheusConnect. "
        "Install it with: pip install prometheus-api-client[async]"
    ) from exc

import asyncio
import bz2
import math
import os

from .exceptions import PrometheusApiClientException


class AsyncPrometheusConnect:
    """
    An asynchronous client for the Prometheus HTTP API.

    The HTTP session is created lazily on the first request.

    :param url: URL of the Prometheus host.
    :param headers: Optional HTTP headers.
    :param disable_ssl: Disable SSL certificate verification when True.
    :param ssl_context: Optional ssl.SSLContext for custom CA or client
        certificate configuration.
    :param auth: Optional aiohttp.BasicAuth instance or (username, password) tuple.
    :param proxy: Optional proxy dictionary.
    :param timeout: Optional request timeout in seconds.
    :param method: HTTP method (GET or POST) for query APIs.
    :param retry: Number of retries for transient request failures.
    :param retry_backoff_factor: Base delay in seconds between retries.
    """

    def __init__(
        self,
        url: str = "http://127.0.0.1:9090",
        headers: Optional[dict] = None,
        disable_ssl: bool = False,
        ssl_context=None,
        auth=None,
        proxy: Optional[dict] = None,
        timeout: Optional[float] = None,
        method: str = "GET",
        retry: int = 3,
        retry_backoff_factor: float = 1.0,
    ):
        """Initialize the asynchronous Prometheus client."""
        if url is None:
            raise TypeError("missing url")

        if not isinstance(url, str):
            raise TypeError("url must be a string")

        if not isinstance(method, str):
            raise TypeError("Method must be a string")

        method = method.upper()
        if method not in {"GET", "POST"}:
            raise ValueError("Method can only be GET or POST")

        if isinstance(retry, bool) or not isinstance(retry, int) or retry < 0:
            raise ValueError("retry must be a non-negative integer")

        if (
            isinstance(retry_backoff_factor, bool)
            or not isinstance(retry_backoff_factor, (int, float))
            or not math.isfinite(retry_backoff_factor)
            or retry_backoff_factor < 0
        ):
            raise ValueError("retry_backoff_factor must be a finite, non-negative number")

        if timeout is not None and (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError("timeout must be a finite, positive number")

        self.url = url.rstrip("/")
        self.prometheus_host = urlparse(self.url).netloc
        self.headers = headers
        self.disable_ssl = disable_ssl
        self.ssl_context = ssl_context
        self.auth = auth
        self.proxy = proxy
        self._timeout = timeout
        self._method = method
        self._retry = retry
        self._retry_backoff_factor = retry_backoff_factor
        self._retry_statuses = {408, 429, 500, 502, 503, 504}
        self._session = None
        self._all_metrics = None

    async def _get_session(self):
        """Create and return the aiohttp session when needed."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(trust_env=True)
        return self._session

    def _get_auth(self):
        """Convert a username/password tuple to aiohttp.BasicAuth."""
        if isinstance(self.auth, tuple):
            return aiohttp.BasicAuth(*self.auth)
        return self.auth

    def _get_proxy(self):
        """Select the configured proxy for the Prometheus URL."""
        if not self.proxy:
            return None

        parsed_url = urlparse(self.url)
        scheme = parsed_url.scheme
        host = parsed_url.netloc

        proxy_keys = (
            "{}://{}".format(scheme, host),
            scheme,
            "all://{}".format(host),
            "all",
            "{}_proxy".format(scheme),
        )

        for key in proxy_keys:
            if key in self.proxy:
                return self.proxy[key]

        return None

    async def _request(self, endpoint: str, params: dict, timeout=None, method=None):
        """Perform an asynchronous request with retry support."""
        session = await self._get_session()

        request_timeout = self._timeout if timeout is None else timeout

        if request_timeout is not None and (
            isinstance(request_timeout, bool)
            or not isinstance(request_timeout, (int, float))
            or not math.isfinite(request_timeout)
            or request_timeout <= 0
        ):
            raise ValueError("timeout must be a finite, positive number")

        request_kwargs = {}
        if request_timeout is not None:
            request_kwargs["timeout"] = aiohttp.ClientTimeout(total=request_timeout)

        request_method = method or self._method
        request_url = "{}/api/v1/{}".format(self.url, endpoint)

        for attempt in range(self._retry + 1):
            retry_delay = None

            try:
                async with session.request(
                    method=request_method,
                    url=request_url,
                    params=params,
                    headers=self.headers,
                    auth=self._get_auth(),
                    proxy=self._get_proxy(),
                    ssl=(
                        self.ssl_context if self.ssl_context is not None else not self.disable_ssl
                    ),
                    **request_kwargs,
                ) as response:
                    if response.status == 200:
                        payload = await response.json()
                        data = payload["data"]

                        if isinstance(data, dict) and "result" in data:
                            return data["result"]

                        return data

                    response_content = await response.read()

                    if response.status in self._retry_statuses and attempt < self._retry:
                        retry_delay = self._retry_backoff_factor * (2**attempt)
                    else:
                        raise PrometheusApiClientException(
                            "HTTP Status Code {} ({!r})".format(response.status, response_content)
                        )

            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt >= self._retry:
                    raise

                retry_delay = self._retry_backoff_factor * (2**attempt)

            if retry_delay is not None:
                await asyncio.sleep(retry_delay)

    async def custom_query(self, query: str, params: Optional[dict] = None, timeout=None):
        """
        Send an instant PromQL query asynchronously.

        :param query: PromQL expression.
        :param params: Optional additional HTTP query parameters.
        :param timeout: Optional request timeout in seconds.
        :returns: List of metric results.
        """
        request_params = {
            **(params or {}),
            "query": str(query),
        }
        return await self._request("query", request_params, timeout)

    async def custom_query_range(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        step: str,
        params: Optional[dict] = None,
        timeout=None,
    ):
        """
        Send a range PromQL query asynchronously.

        :param query: PromQL expression.
        :param start_time: Range start datetime.
        :param end_time: Range end datetime.
        :param step: Query resolution step.
        :param params: Optional additional HTTP query parameters.
        :param timeout: Optional request timeout in seconds.
        :returns: List of metric results.
        """
        request_params = {
            **(params or {}),
            "query": str(query),
            "start": round(start_time.timestamp()),
            "end": round(end_time.timestamp()),
            "step": step,
        }
        return await self._request("query_range", request_params, timeout)

    async def check_prometheus_connection(self, params: dict = None) -> bool:
        """Check whether the Prometheus endpoint is reachable."""
        session = await self._get_session()

        request_kwargs = {}
        if self._timeout is not None:
            request_kwargs["timeout"] = aiohttp.ClientTimeout(total=self._timeout)

        async with session.request(
            method="GET",
            url="{}/".format(self.url),
            headers=self.headers,
            params=params,
            auth=self._get_auth(),
            proxy=self._get_proxy(),
            ssl=(self.ssl_context if self.ssl_context is not None else not self.disable_ssl),
            **request_kwargs,
        ) as response:
            return response.ok

    async def all_metrics(self, params: dict = None):
        """Get all metric names scraped by Prometheus."""
        self._all_metrics = await self.get_label_values(label_name="__name__", params=params)
        return self._all_metrics

    async def get_series(self, start: datetime, end: datetime, params: dict = None):
        """Get series between the supplied start and end times."""
        request_params = {
            **(params or {}),
            "start": start.timestamp(),
            "end": end.timestamp(),
        }
        return await self._request(
            "series",
            request_params,
            method="GET",
        )

    async def get_label_names(self, params: dict = None):
        """Get all label names."""
        return await self._request("labels", params or {})

    async def get_label_values(self, label_name: str, params: dict = None):
        """Get all values for a label."""
        return await self._request(
            "label/{}/values".format(label_name),
            params or {},
            method="GET",
        )

    async def get_current_metric_value(
        self, metric_name: str, label_config: dict = None, params: dict = None
    ):
        """Get the current value of a metric with optional label filters."""
        if label_config:
            label_list = ["{}='{}'".format(key, label_config[key]) for key in label_config]
            query = "{}{{{}}}".format(metric_name, ",".join(label_list))
        else:
            query = metric_name

        return await self.custom_query(query=query, params=params)

    async def get_metric_range_data(
        self,
        metric_name: str,
        label_config: dict = None,
        start_time: datetime = None,
        end_time: datetime = None,
        chunk_size: timedelta = None,
        store_locally: bool = False,
        params: dict = None,
    ):
        """Get metric values over a time range, optionally in chunks."""
        params = params or {}
        data = []

        if start_time is None:
            start_time = datetime.now() - timedelta(minutes=10)
        if end_time is None:
            end_time = datetime.now()

        if not (isinstance(start_time, datetime) and isinstance(end_time, datetime)):
            raise TypeError("start_time and end_time can only be of type datetime.datetime")

        if chunk_size is None:
            chunk_size = end_time - start_time

        if not isinstance(chunk_size, timedelta):
            raise TypeError("chunk_size can only be of type datetime.timedelta")

        if end_time < start_time:
            raise ValueError("end_time must not be before start_time")

        if (end_time - start_time).total_seconds() < chunk_size.total_seconds():
            raise ValueError("specified chunk_size is too big")

        chunk_seconds = round(chunk_size.total_seconds())
        if chunk_seconds <= 0:
            raise ValueError("chunk_size must be greater than zero")

        start = round(start_time.timestamp())
        end = round(end_time.timestamp())

        if label_config:
            label_list = ["{}='{}'".format(key, label_config[key]) for key in label_config]
            query = "{}{{{}}}".format(metric_name, ",".join(label_list))
        else:
            query = metric_name

        while start < end:
            current_chunk = min(chunk_seconds, end - start)

            result = await self.custom_query(
                query=query + "[{}s]".format(current_chunk),
                params={
                    **params,
                    "time": start + current_chunk,
                },
            )

            data.extend(result)

            if store_locally:
                import json

                self._store_metric_values_local(
                    metric_name,
                    json.dumps(result),
                    start + current_chunk,
                )

            start += current_chunk

        return data

    async def get_metric_aggregation(
        self,
        query: str,
        operations: list,
        start_time: datetime = None,
        end_time: datetime = None,
        step: str = "15",
        params: dict = None,
    ):
        """Get aggregations on metric values received from a PromQL query."""
        try:
            import numpy
        except ImportError as e:
            raise ImportError(
                "NumPy is required for metric aggregation operations. "
                "Please install it with: pip install prometheus-api-client[analytics] "
                "or pip install prometheus-api-client[all]"
            ) from e

        if not isinstance(operations, list):
            raise TypeError("Operations can be only of type list")

        if len(operations) == 0:
            return None

        query_values = []

        if start_time is not None and end_time is not None:
            data = await self.custom_query_range(
                query=query,
                params=params,
                start_time=start_time,
                end_time=end_time,
                step=step,
            )
            for result in data:
                for value in result["values"]:
                    query_values.append(float(value[1]))
        else:
            data = await self.custom_query(query, params)
            for result in data:
                query_values.append(float(result["value"][1]))

        if not query_values:
            return None

        np_array = numpy.array(query_values)
        aggregated_values = {}

        for operation in operations:
            if operation == "sum":
                aggregated_values["sum"] = numpy.sum(np_array)
            elif operation == "max":
                aggregated_values["max"] = numpy.max(np_array)
            elif operation == "min":
                aggregated_values["min"] = numpy.min(np_array)
            elif operation == "average":
                aggregated_values["average"] = numpy.average(np_array)
            elif operation.startswith("percentile"):
                percentile = float(operation.split("_")[1])
                aggregated_values["percentile_" + str(percentile)] = numpy.percentile(
                    query_values, percentile
                )
            elif operation == "deviation":
                aggregated_values["deviation"] = numpy.std(np_array)
            elif operation == "variance":
                aggregated_values["variance"] = numpy.var(np_array)
            else:
                raise TypeError("Invalid operation: " + operation)

        return aggregated_values

    async def get_scrape_pools(self):
        """Get a list of all scrape pools in active targets."""
        targets = await self.get_targets()
        return list({target["scrapePool"] for target in targets["activeTargets"]})

    async def get_targets(self, state: str = None, scrape_pool: str = None):
        """
        Get targets from Prometheus.

        :param state: Optional target state ('active', 'dropped', or 'any').
        :param scrape_pool: Optional scrape pool name.
        :returns: Dictionary containing active and dropped targets.
        """
        params = {}

        if state:
            params["state"] = state

        if scrape_pool:
            params["scrapePool"] = scrape_pool

        return await self._request("targets", params, method="GET")

    async def get_target_metadata(self, target: dict, metric: str = None):
        """
        Get metadata about metrics from a specific target.

        :param target: Target labels to match.
        :param metric: Optional metric name filter.
        :returns: List of matching metadata entries.
        """
        params = {}

        if metric:
            params["metric"] = metric

        if target:
            match_target = "{" + ",".join(f'{key}="{value}"' for key, value in target.items()) + "}"
            params["match_target"] = match_target

        return await self._request("targets/metadata", params, method="GET")

    async def get_metric_metadata(
        self, metric: str = None, limit: int = None, limit_per_metric: int = None
    ):
        """
        Get metadata about metrics.

        :param metric: Optional metric name filter.
        :param limit: Optional maximum number of metrics.
        :param limit_per_metric: Optional maximum entries per metric.
        :returns: List of formatted metadata entries.
        """
        params = {}

        if metric:
            params["metric"] = metric

        if limit:
            params["limit"] = limit

        if limit_per_metric:
            params["limit_per_metric"] = limit_per_metric

        data = await self._request("metadata", params, method="GET")

        formatted_data = []

        for metric_name, entries in data.items():
            for entry in entries:
                formatted_data.append(
                    {
                        "metric_name": metric_name,
                        "type": entry.get("type", "unknown"),
                        "help": entry.get("help", ""),
                        "unit": entry.get("unit", ""),
                    }
                )

        return formatted_data

    def _store_metric_values_local(self, metric_name, values, end_timestamp, compressed=False):
        """Store metric values locally, optionally using bz2 compression."""
        if not values:
            return None

        file_path = self._metric_filename(metric_name, end_timestamp)

        if compressed:
            payload = bz2.compress(str(values).encode("utf-8"))
            file_path += ".bz2"
        else:
            payload = str(values).encode("utf-8")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(payload)

        return file_path

    def _metric_filename(self, metric_name: str, end_timestamp: int):
        """Generate the local metric filename."""
        end_time_stamp = datetime.fromtimestamp(end_timestamp)
        directory_name = end_time_stamp.strftime("%Y%m%d")
        timestamp = end_time_stamp.strftime("%Y%m%d%H%M")

        return os.path.join(
            ".",
            "metrics",
            self.prometheus_host,
            metric_name,
            directory_name,
            timestamp + ".json",
        )

    async def close(self):
        """Close the underlying HTTP session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Support async context-manager usage."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the session when leaving the async context."""
        await self.close()
