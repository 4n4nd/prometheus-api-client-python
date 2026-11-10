import unittest
from datetime import datetime, timedelta, timezone

from aiohttp import web
from aiohttp.test_utils import TestServer

from prometheus_api_client import AsyncPrometheusConnect
from prometheus_api_client.exceptions import PrometheusApiClientException


class TestAsyncPrometheusConnect(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.requests = []
        self.retry_attempts = 0

        async def handler(request):
            self.requests.append(request)

            if request.path == "/":
                return web.Response(status=200)

            if request.query.get("query") == "retry_query":
                self.retry_attempts += 1

                if self.retry_attempts == 1:
                    return web.Response(status=503)

                return web.json_response(
                    {
                        "status": "success",
                        "data": {
                            "resultType": "vector",
                            "result": [{"value": 1}],
                        },
                    }
                )

            if request.query.get("query") == "bad_query":
                return web.json_response(
                    {"status": "error", "error": "bad query"},
                    status=400,
                )

            if request.path.endswith("/api/v1/query") and "[" in request.query.get("query", ""):
                return web.json_response(
                    {
                        "status": "success",
                        "data": {
                            "resultType": "vector",
                            "result": [{"metric": {"__name__": "up"}, "value": [1, "1"]}],
                        },
                    }
                )

            if request.path.endswith("/api/v1/query"):
                if request.query.get("query") == "aggregation_query":
                    return web.json_response(
                        {
                            "status": "success",
                            "data": {
                                "resultType": "vector",
                                "result": [
                                    {"metric": {"__name__": "up"}, "value": [1, "10"]},
                                    {"metric": {"__name__": "up"}, "value": [2, "20"]},
                                    {"metric": {"__name__": "up"}, "value": [3, "30"]},
                                ],
                            },
                        }
                    )

                return web.json_response(
                    {
                        "status": "success",
                        "data": {"resultType": "vector", "result": [{"value": 1}]},
                    }
                )

            if request.path.endswith("/api/v1/query_range"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": {
                            "resultType": "matrix",
                            "result": [{"values": [[1, "10"], [2, "20"], [3, "30"]]}],
                        },
                    }
                )

            if request.path.endswith("/api/v1/labels"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": ["job", "instance"],
                    }
                )

            if request.path.endswith("/api/v1/label/__name__/values"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": ["up", "process_cpu_seconds_total"],
                    }
                )

            if request.path.endswith("/api/v1/series"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": [{"__name__": "up", "job": "prometheus"}],
                    }
                )

            if request.path.endswith("/api/v1/targets/metadata"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": [
                            {"metric": "up", "type": "gauge"},
                        ],
                    }
                )

            if request.path.endswith("/api/v1/targets"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": {
                            "activeTargets": [
                                {"scrapePool": "prometheus"},
                                {"scrapePool": "node"},
                            ],
                            "droppedTargets": [],
                        },
                    }
                )

            if request.path.endswith("/api/v1/metadata"):
                return web.json_response(
                    {
                        "status": "success",
                        "data": {
                            "up": [
                                {
                                    "type": "gauge",
                                    "help": "Target is up",
                                    "unit": "",
                                }
                            ]
                        },
                    }
                )

            return web.Response(status=404)

        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", handler)

        self.server = TestServer(app)
        await self.server.start_server()

        self.prom = AsyncPrometheusConnect(url=str(self.server.make_url("")))

    async def asyncTearDown(self):
        await self.prom.close()
        await self.server.close()

    async def test_check_prometheus_connection(self):
        result = await self.prom.check_prometheus_connection()
        self.assertTrue(result)

    async def test_all_metrics(self):
        result = await self.prom.all_metrics()
        self.assertEqual(result, ["up", "process_cpu_seconds_total"])

    async def test_get_series(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 2, tzinfo=timezone.utc)

        result = await self.prom.get_series(start, end)

        self.assertEqual(result[0]["__name__"], "up")
        self.assertIn("start", self.requests[-1].query)
        self.assertIn("end", self.requests[-1].query)

    async def test_get_label_names(self):
        result = await self.prom.get_label_names()
        self.assertEqual(result, ["job", "instance"])

    async def test_get_label_values(self):
        result = await self.prom.get_label_values("__name__")
        self.assertEqual(result, ["up", "process_cpu_seconds_total"])

    async def test_get_label_values_uses_get(self):
        await self.prom.get_label_values("__name__")
        self.assertEqual(self.requests[-1].method, "GET")

    async def test_get_current_metric_value(self):
        result = await self.prom.get_current_metric_value("up")
        self.assertEqual(result, [{"value": 1}])

    async def test_http_error(self):
        with self.assertRaises(PrometheusApiClientException):
            await self.prom.custom_query("bad_query")

    async def test_get_metric_range_data(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 0, 2, tzinfo=timezone.utc)

        result = await self.prom.get_metric_range_data(
            metric_name="up",
            start_time=start,
            end_time=end,
            chunk_size=timedelta(minutes=1),
        )

        self.assertEqual(len(result), 2)

    async def test_get_metric_range_data_invalid_chunk(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 0, 2, tzinfo=timezone.utc)

        with self.assertRaises(ValueError):
            await self.prom.get_metric_range_data(
                metric_name="up",
                start_time=start,
                end_time=end,
                chunk_size=timedelta(minutes=3),
            )

    async def test_get_targets(self):
        result = await self.prom.get_targets(state="active")
        self.assertEqual(len(result["activeTargets"]), 2)
        self.assertEqual(self.requests[-1].query["state"], "active")

    async def test_get_scrape_pools(self):
        result = await self.prom.get_scrape_pools()
        self.assertEqual(set(result), {"prometheus", "node"})

    async def test_get_target_metadata(self):
        result = await self.prom.get_target_metadata({"job": "prometheus"}, metric="up")
        self.assertEqual(result[0]["metric"], "up")
        self.assertEqual(
            self.requests[-1].query["match_target"],
            '{job="prometheus"}',
        )

    async def test_get_metric_metadata(self):
        result = await self.prom.get_metric_metadata(metric="up")
        self.assertEqual(
            result,
            [
                {
                    "metric_name": "up",
                    "type": "gauge",
                    "help": "Target is up",
                    "unit": "",
                }
            ],
        )

    async def test_retries_on_server_error(self):
        client = AsyncPrometheusConnect(
            url=str(self.server.make_url("")),
            retry=1,
            retry_backoff_factor=0,
        )

        try:
            result = await client.custom_query("retry_query")

            self.assertEqual(result, [{"value": 1}])
            self.assertEqual(self.retry_attempts, 2)
        finally:
            await client.close()

    async def test_get_metric_aggregation_instant_query(self):
        result = await self.prom.get_metric_aggregation(
            query="aggregation_query",
            operations=["sum", "max", "min", "average", "deviation", "variance", "percentile_50"],
        )

        self.assertEqual(result["sum"], 60)
        self.assertEqual(result["max"], 30)
        self.assertEqual(result["min"], 10)
        self.assertEqual(result["average"], 20)
        self.assertEqual(result["percentile_50.0"], 20)
        self.assertAlmostEqual(result["deviation"], 8.16496580927726)
        self.assertAlmostEqual(result["variance"], 66.66666666666667)

    async def test_get_metric_aggregation_range_query(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 2, tzinfo=timezone.utc)

        result = await self.prom.get_metric_aggregation(
            query="aggregation_query",
            operations=["sum", "average"],
            start_time=start,
            end_time=end,
        )

        self.assertEqual(result["sum"], 60)
        self.assertEqual(result["average"], 20)

    async def test_get_metric_aggregation_empty_operations(self):
        result = await self.prom.get_metric_aggregation(
            query="up",
            operations=[],
        )

        self.assertIsNone(result)

    async def test_get_metric_aggregation_invalid_operation(self):
        with self.assertRaises(TypeError):
            await self.prom.get_metric_aggregation(
                query="up",
                operations=["invalid"],
            )

    async def test_get_metric_aggregation_invalid_operations_type(self):
        with self.assertRaises(TypeError):
            await self.prom.get_metric_aggregation(
                query="up",
                operations="sum",
            )

    async def test_session_created_lazily(self):
        client = AsyncPrometheusConnect(url=str(self.server.make_url("")))

        self.assertIsNone(client._session)

        try:
            await client.custom_query("up")
            self.assertIsNotNone(client._session)
            self.assertFalse(client._session.closed)
        finally:
            await client.close()

    async def test_close_and_recreate_session(self):
        await self.prom.custom_query("up")
        original_session = self.prom._session

        await self.prom.close()
        self.assertTrue(original_session.closed)

        await self.prom.custom_query("up")

        self.assertIsNot(self.prom._session, original_session)
        self.assertFalse(self.prom._session.closed)

    async def test_async_context_manager_closes_session(self):
        client = AsyncPrometheusConnect(url=str(self.server.make_url("")))

        async with client as prom:
            await prom.custom_query("up")
            self.assertFalse(prom._session.closed)

        self.assertTrue(client._session.closed)

    async def test_constructor_validation(self):
        invalid_options = [
            {"retry": True},
            {"retry": -1},
            {"retry_backoff_factor": -1},
            {"retry_backoff_factor": float("nan")},
            {"retry_backoff_factor": float("inf")},
            {"timeout": -1},
            {"timeout": float("inf")},
        ]

        for options in invalid_options:
            with self.subTest(options=options):
                with self.assertRaises(ValueError):
                    AsyncPrometheusConnect(**options)

        with self.assertRaises(TypeError):
            AsyncPrometheusConnect(url=None)

    async def test_post_method(self):
        client = AsyncPrometheusConnect(
            url=str(self.server.make_url("")),
            method="POST",
        )

        try:
            await client.custom_query("up")
            self.assertEqual(self.requests[-1].method, "POST")
        finally:
            await client.close()

    async def test_non_retryable_http_error_is_not_retried(self):
        client = AsyncPrometheusConnect(
            url=str(self.server.make_url("")),
            retry=3,
            retry_backoff_factor=0,
        )

        try:
            request_count_before = len(self.requests)

            with self.assertRaises(PrometheusApiClientException):
                await client.custom_query("bad_query")

            self.assertEqual(
                len(self.requests) - request_count_before,
                1,
            )
        finally:
            await client.close()

    async def test_custom_query_does_not_allow_params_to_override_query(self):
        await self.prom.custom_query(
            "up",
            params={"query": "different_query"},
        )

        self.assertEqual(self.requests[-1].query["query"], "up")

    async def test_get_metric_range_data_rejects_zero_chunk_size(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 0, 2, tzinfo=timezone.utc)

        with self.assertRaises(ValueError):
            await self.prom.get_metric_range_data(
                metric_name="up",
                start_time=start,
                end_time=end,
                chunk_size=timedelta(0),
            )

    async def test_get_series_uses_get_with_post_configuration(self):
        client = AsyncPrometheusConnect(
            url=str(self.server.make_url("")),
            method="POST",
        )

        try:
            start = datetime(2026, 1, 1, tzinfo=timezone.utc)
            end = datetime(2026, 1, 2, tzinfo=timezone.utc)

            await client.get_series(start, end)

            self.assertEqual(self.requests[-1].method, "GET")
        finally:
            await client.close()

    async def test_request_rejects_invalid_timeout(self):
        client = AsyncPrometheusConnect()

        try:
            for timeout in (-1, float("inf"), float("nan"), True, "invalid"):
                with self.subTest(timeout=timeout):
                    with self.assertRaises(ValueError):
                        await client._request("query", {}, timeout=timeout)
        finally:
            await client.close()


if __name__ == "__main__":
    unittest.main()
