# tests/test_gvp.py
import unittest
from volcanoes import GVP


class TestGVP(unittest.TestCase):
    def setUp(self):
        self.gvp = GVP()

    def test_load_data(self):
        self.assertGreater(len(self.gvp.volcanoes), 0)

    def test_filter_by_country(self):
        italy = self.gvp.filter_volcanoes(country="Italy")
        self.assertGreater(len(italy), 0)


if __name__ == '__main__':
    unittest.main()