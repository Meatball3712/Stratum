import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Farm

class NorthernFarm(Farm):
    """docstring for NorthernFarm"""
    def __init__(self, **kwargs):
        super().__init__(name="Northern Farm", **kwargs)
