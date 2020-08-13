"""Disk caching helper PrometheusConnect """
import json
import os
import tempfile

class DiskCache:
    """A disk cache class for PrometheusConnect """
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            self.cache_dir = tempfile.mkdtemp(prefix='prom')
        else:
            self.cache_dir = cache_dir


    def load(self, key):
        """ Load data under given key. """
        path = os.path.join(self.cache_dir, key)
        if os.path.exists(path):
            with open(path) as file:
                return json.load(file)
        return None


    def store(self, key, data):
        """ Store data under given key. """
        path = os.path.join(self.cache_dir, key)
        with open(path, 'w') as file:
            return json.dump(data, file)
        return None

