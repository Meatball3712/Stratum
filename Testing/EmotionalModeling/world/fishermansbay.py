import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Village

class FishermansBay(Village):
    """docstring for FishermansBay"""
    def __init__(self, **kwargs):
        super().__init__(name="Fishermans Bay", **kwargs)
