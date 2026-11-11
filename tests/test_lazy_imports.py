"""Test lazy imports to ensure pandas/matplotlib are not loaded unnecessarily."""

import unittest
import sys
import subprocess


class TestLazyImports(unittest.TestCase):
    """Test that PrometheusConnect can be imported without loading
    heavy dependencies.
    """

    def _run_in_subprocess(self, code, fail_map):
        """Run code in a subprocess and check exit codes against fail_map.

        Args:
            code: Python code to execute in subprocess
            fail_map: Dictionary mapping exit codes to error messages

        Raises:
            AssertionError: If subprocess exits with a code in fail_map
            or any non-zero code
        """
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )

        if result.returncode in fail_map:
            self.fail(fail_map[result.returncode])
        elif result.returncode != 0:
            # Include both stdout and stderr for better debugging
            output = []
            if result.stdout:
                output.append(f"stdout: {result.stdout}")
            if result.stderr:
                output.append(f"stderr: {result.stderr}")
            output_str = "\n".join(output) if output else "no output"
            self.fail(f"Subprocess failed with code {result.returncode}: {output_str}")

    def test_prometheus_connect_import_without_pandas_matplotlib_numpy(self):
        """Test that importing PrometheusConnect doesn't load pandas,
        matplotlib, or numpy.
        """
        # Run in a subprocess to avoid affecting other tests
        code = """
import sys
from prometheus_api_client import PrometheusConnect

# Check that pandas, matplotlib, and numpy are not loaded
pandas_loaded = any(
    m == 'pandas' or m.startswith('pandas.') for m in sys.modules.keys()
)
matplotlib_loaded = any(
    m == 'matplotlib' or m.startswith('matplotlib.') for m in sys.modules.keys()
)
numpy_loaded = any(
    m == 'numpy' or m.startswith('numpy.') for m in sys.modules.keys()
)
aiohttp_loaded = any(
    m == 'aiohttp' or m.startswith('aiohttp.') for m in sys.modules.keys()
)

if pandas_loaded:
    sys.exit(1)
if matplotlib_loaded:
    sys.exit(2)
if numpy_loaded:
    sys.exit(3)
if aiohttp_loaded:
    sys.exit(4)
sys.exit(0)
"""
        fail_map = {
            1: "pandas should not be loaded when importing PrometheusConnect",
            2: "matplotlib should not be loaded when importing PrometheusConnect",
            3: "numpy should not be loaded when importing PrometheusConnect",
            4: "aiohttp should not be loaded when importing PrometheusConnect",
        }
        self._run_in_subprocess(code, fail_map)

    def test_prometheus_connect_instantiation_without_numpy(self):
        """Test that PrometheusConnect can be instantiated without loading numpy."""
        # Run in a subprocess to avoid affecting other tests
        code = """
import sys
from prometheus_api_client import PrometheusConnect

pc = PrometheusConnect(url='http://test.local:9090')

# Check that numpy is still not loaded after instantiation
numpy_loaded = any(m == 'numpy' or m.startswith('numpy.') for m in sys.modules.keys())

if numpy_loaded:
    sys.exit(1)
if pc is None:
    sys.exit(2)
sys.exit(0)
"""
        fail_map = {
            1: "numpy should not be loaded when instantiating PrometheusConnect",
            2: "PrometheusConnect should be instantiated successfully",
        }
        self._run_in_subprocess(code, fail_map)

    def test_metric_import_loads_pandas(self):
        """Test that importing Metric does load pandas (expected behavior)."""
        # This test doesn't remove modules, so it won't cause reload issues
        from prometheus_api_client import Metric  # noqa: F401

        # Check that pandas is loaded (this is expected for Metric)
        pandas_loaded = any(m == "pandas" or m.startswith("pandas.") for m in sys.modules.keys())
        self.assertTrue(pandas_loaded, "pandas should be loaded when importing Metric")

    def test_async_import_without_aiohttp_shows_install_message(self):
        """Test that importing AsyncPrometheusConnect gives a helpful error
        without aiohttp.
        """
        code = """
import builtins
import sys

real_import = builtins.__import__

def blocked_import(name, *args, **kwargs):
    if name == "aiohttp" or name.startswith("aiohttp."):
        raise ImportError("aiohttp blocked for test")
    return real_import(name, *args, **kwargs)

builtins.__import__ = blocked_import

try:
    from prometheus_api_client import AsyncPrometheusConnect
except ImportError as exc:
    if "pip install prometheus-api-client[async]" not in str(exc):
        sys.exit(1)
else:
    sys.exit(2)

sys.exit(0)
"""
        fail_map = {
            1: "The aiohttp import error should explain how to install the async extra",
            2: ("Importing AsyncPrometheusConnect should fail when " "aiohttp is unavailable"),
        }
        self._run_in_subprocess(code, fail_map)


if __name__ == "__main__":
    unittest.main()
