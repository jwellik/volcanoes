# tests/test_gvp.py
import unittest
import tempfile
import os
import shutil
from pathlib import Path
from volcanoes import GVP


class TestGVP(unittest.TestCase):
    def setUp(self):
        # Use a temporary cache directory for testing
        self.test_cache_dir = tempfile.mkdtemp(prefix='volcanoes_test_cache_')
        self.gvp = GVP(cache_dir=self.test_cache_dir)
    
    def tearDown(self):
        # Clean up test cache directory
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir, ignore_errors=True)

    def test_load_data(self):
        self.assertGreater(len(self.gvp.volcanoes), 0)

    def test_filter_by_country(self):
        italy = self.gvp.filter_volcanoes(country="Italy")
        self.assertGreater(len(italy), 0)


if __name__ == '__main__':
    unittest.main()