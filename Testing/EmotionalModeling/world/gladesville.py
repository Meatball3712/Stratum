import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Village

class Gladesville(Village):
    """docstring for Gladesville"""
    def __init__(self, **kwargs):
        super().__init__(name="Gladesville", **kwargs)
