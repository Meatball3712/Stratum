import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Farm

class WesternFarm(Farm):
    """docstring for WesternFarm"""
    def __init__(self, **kwargs):
        super().__init__(name="Western Farm", **kwargs)
