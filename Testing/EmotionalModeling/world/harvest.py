import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Village

class Harvest(Village):
    """docstring for Harvest"""
    def __init__(self, **kwargs):
        super().__init__(name="Harvest", **kwargs)
