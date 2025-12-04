"""Test lazy imports to ensure pandas/matplotlib are not loaded unnecessarily."""
import unittest
import sys
import importlib


class TestLazyImports(unittest.TestCase):
    """Test that PrometheusConnect can be imported without loading heavy dependencies."""

    @staticmethod
    def _remove_modules(module_names):
        """Remove specified modules and their submodules from sys.modules.
        
        Args:
            module_names: List of module names to remove
        """
        for module_name in module_names:
            modules_to_remove = [
                key for key in sys.modules.keys()
                if key == module_name or key.startswith(module_name + '.')
            ]
            for module in modules_to_remove:
                del sys.modules[module]
    
    @staticmethod
    def _is_module_loaded(module_name):
        """Check if a module is loaded in sys.modules.
        
        Args:
            module_name: Name of the module to check
            
        Returns:
            bool: True if module is loaded, False otherwise
        """
        return any(m == module_name or m.startswith(module_name + '.') for m in sys.modules.keys())

    def test_prometheus_connect_import_without_pandas_matplotlib_numpy(self):
        """Test that importing PrometheusConnect doesn't load pandas, matplotlib, or numpy."""
        # Remove any previously loaded modules
        self._remove_modules(['prometheus_api_client', 'numpy', 'pandas', 'matplotlib'])
        
        # Import PrometheusConnect
        from prometheus_api_client import PrometheusConnect
        
        # Check that pandas, matplotlib, and numpy are not loaded
        self.assertFalse(self._is_module_loaded('pandas'), 
                        "pandas should not be loaded when importing PrometheusConnect")
        self.assertFalse(self._is_module_loaded('matplotlib'), 
                        "matplotlib should not be loaded when importing PrometheusConnect")
        self.assertFalse(self._is_module_loaded('numpy'), 
                        "numpy should not be loaded when importing PrometheusConnect")
        
    def test_prometheus_connect_instantiation_without_numpy(self):
        """Test that PrometheusConnect can be instantiated without loading numpy."""
        # Remove any previously loaded modules
        self._remove_modules(['prometheus_api_client', 'numpy'])
        
        # Import and instantiate PrometheusConnect
        from prometheus_api_client import PrometheusConnect
        pc = PrometheusConnect(url='http://test.local:9090')
        
        # Check that numpy is still not loaded after instantiation
        self.assertFalse(self._is_module_loaded('numpy'), 
                        "numpy should not be loaded when instantiating PrometheusConnect")
        self.assertIsNotNone(pc, "PrometheusConnect should be instantiated successfully")

    def test_metric_import_loads_pandas(self):
        """Test that importing Metric does load pandas (expected behavior)."""
        # Remove any previously loaded modules
        self._remove_modules(['prometheus_api_client', 'pandas'])
        
        # Import Metric
        from prometheus_api_client import Metric
        
        # Check that pandas is loaded (this is expected for Metric)
        self.assertTrue(self._is_module_loaded('pandas'), 
                       "pandas should be loaded when importing Metric")


if __name__ == '__main__':
    unittest.main()
