"""Test lazy imports to ensure pandas/matplotlib are not loaded unnecessarily."""
import unittest
import sys
import importlib


class TestLazyImports(unittest.TestCase):
    """Test that PrometheusConnect can be imported without loading heavy dependencies."""

    def test_prometheus_connect_import_without_pandas_matplotlib_numpy(self):
        """Test that importing PrometheusConnect doesn't load pandas, matplotlib, or numpy."""
        # Remove any previously loaded prometheus_api_client modules
        modules_to_remove = [
            key for key in sys.modules.keys()
            if key.startswith('prometheus_api_client')
        ]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Also remove numpy, pandas, matplotlib if they were loaded
        for heavy_module in ['numpy', 'pandas', 'matplotlib']:
            modules_to_remove = [
                key for key in sys.modules.keys()
                if key == heavy_module or key.startswith(heavy_module + '.')
            ]
            for module in modules_to_remove:
                del sys.modules[module]
        
        # Import PrometheusConnect
        from prometheus_api_client import PrometheusConnect
        
        # Check that pandas, matplotlib, and numpy are not loaded
        loaded_modules = sys.modules.keys()
        pandas_loaded = any('pandas' in m for m in loaded_modules)
        matplotlib_loaded = any('matplotlib' in m for m in loaded_modules)
        numpy_loaded = any('numpy' in m for m in loaded_modules)
        
        self.assertFalse(pandas_loaded, "pandas should not be loaded when importing PrometheusConnect")
        self.assertFalse(matplotlib_loaded, "matplotlib should not be loaded when importing PrometheusConnect")
        self.assertFalse(numpy_loaded, "numpy should not be loaded when importing PrometheusConnect")
        
    def test_prometheus_connect_instantiation_without_numpy(self):
        """Test that PrometheusConnect can be instantiated without loading numpy."""
        # Remove any previously loaded prometheus_api_client modules
        modules_to_remove = [
            key for key in sys.modules.keys()
            if key.startswith('prometheus_api_client')
        ]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Also remove numpy if it was loaded
        modules_to_remove = [
            key for key in sys.modules.keys()
            if key == 'numpy' or key.startswith('numpy.')
        ]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Import and instantiate PrometheusConnect
        from prometheus_api_client import PrometheusConnect
        pc = PrometheusConnect(url='http://test.local:9090')
        
        # Check that numpy is still not loaded after instantiation
        loaded_modules = sys.modules.keys()
        numpy_loaded = any('numpy' in m for m in loaded_modules)
        
        self.assertFalse(numpy_loaded, "numpy should not be loaded when instantiating PrometheusConnect")
        self.assertIsNotNone(pc, "PrometheusConnect should be instantiated successfully")

    def test_metric_import_loads_pandas(self):
        """Test that importing Metric does load pandas (expected behavior)."""
        # Remove any previously loaded prometheus_api_client modules
        modules_to_remove = [
            key for key in sys.modules.keys()
            if key.startswith('prometheus_api_client')
        ]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Also remove pandas if it was loaded
        modules_to_remove = [
            key for key in sys.modules.keys()
            if key == 'pandas' or key.startswith('pandas.')
        ]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Import Metric
        from prometheus_api_client import Metric
        
        # Check that pandas is loaded (this is expected for Metric)
        loaded_modules = sys.modules.keys()
        pandas_loaded = any('pandas' in m for m in loaded_modules)
        
        self.assertTrue(pandas_loaded, "pandas should be loaded when importing Metric")


if __name__ == '__main__':
    unittest.main()
