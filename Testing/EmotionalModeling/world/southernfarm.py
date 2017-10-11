import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Farm

class SouthernFarm(Farm):
    """docstring for SouthernFarm"""
    def __init__(self, **kwargs):
        super().__init__(name="Southern Farm", **kwargs)
