from django.utils import unittest
from .models import *

class OceanStorySectionTestCase(unittest.TestCase):
    def setUp(self):
        self.section = OceanStorySection()

    def testJsonMapState(self):
        self.section.map_state = "{}"
        self.assertEqual(self.section.parsed_map_state, {})

    def testUrlMapState(self):
        self.section.map_state = "http://portal.midatlanticocean.org/planner/#x=-73.24&y=38.93&z=7&logo=true&controls=true&basemap=ESRI+Ocean&tab=data&legends=false&layers=true"
        self.assertEqual(self.section.parsed_map_state, {
            'baseLayer': 'ESRI Ocean',
            'dataLayers': {},
            'view': {
                'center': ('-73.24', '38.93'),
                'zoom': '7',
            },
        })

    def testLongUrlMapState(self):
        self.section.map_state = "http://portal.midatlanticocean.org/planner/#x=-74.44&y=39.32&z=8&logo=true&controls=true&dls%5B%5D=true&dls%5B%5D=1&dls%5B%5D=20&dls%5B%5D=true&dls%5B%5D=0.5&dls%5B%5D=12&basemap=ESRI+Ocean&themes%5Bids%5D%5B%5D=4&tab=data&legends=false&layers=true"
        self.assertEqual(self.section.parsed_map_state, {
            'baseLayer': 'ESRI Ocean',
            'dataLayers': {'1': {}, '12': {}, '20': {}},
            'view': {'center': ('-74.44', '39.32'), 'zoom': '8'}
        })

    def testInvalidUrlMapState(self):
        # missing x param
        self.section.map_state = "http://portal.midatlanticocean.org/planner/#y=38.93&z=7&logo=true&controls=true&basemap=ESRI+Ocean&tab=data&legends=false&layers=true"
        with self.assertRaises(KeyError):
            self.section.parsed_map_state
