"""Test lazy imports to ensure pandas/matplotlib are not loaded unnecessarily."""
import unittest
import sys
import subprocess
import importlib


class TestLazyImports(unittest.TestCase):
    """Test that PrometheusConnect can be imported without loading heavy dependencies."""

    def test_prometheus_connect_import_without_pandas_matplotlib_numpy(self):
        """Test that importing PrometheusConnect doesn't load pandas, matplotlib, or numpy."""
        # Run in a subprocess to avoid affecting other tests
        code = """
import sys
from prometheus_api_client import PrometheusConnect

# Check that pandas, matplotlib, and numpy are not loaded
pandas_loaded = any(m == 'pandas' or m.startswith('pandas.') for m in sys.modules.keys())
matplotlib_loaded = any(m == 'matplotlib' or m.startswith('matplotlib.') for m in sys.modules.keys())
numpy_loaded = any(m == 'numpy' or m.startswith('numpy.') for m in sys.modules.keys())

if pandas_loaded:
    sys.exit(1)
if matplotlib_loaded:
    sys.exit(2)
if numpy_loaded:
    sys.exit(3)
sys.exit(0)
"""
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 1:
            self.fail("pandas should not be loaded when importing PrometheusConnect")
        elif result.returncode == 2:
            self.fail("matplotlib should not be loaded when importing PrometheusConnect")
        elif result.returncode == 3:
            self.fail("numpy should not be loaded when importing PrometheusConnect")
        elif result.returncode != 0:
            self.fail(f"Subprocess failed with code {result.returncode}: {result.stderr}")
        
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
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 1:
            self.fail("numpy should not be loaded when instantiating PrometheusConnect")
        elif result.returncode == 2:
            self.fail("PrometheusConnect should be instantiated successfully")
        elif result.returncode != 0:
            self.fail(f"Subprocess failed with code {result.returncode}: {result.stderr}")

    def test_metric_import_loads_pandas(self):
        """Test that importing Metric does load pandas (expected behavior)."""
        # This test doesn't remove modules, so it won't cause reload issues
        from prometheus_api_client import Metric
        
        # Check that pandas is loaded (this is expected for Metric)
        pandas_loaded = any(m == 'pandas' or m.startswith('pandas.') for m in sys.modules.keys())
        self.assertTrue(pandas_loaded, "pandas should be loaded when importing Metric")


if __name__ == '__main__':
    unittest.main()
