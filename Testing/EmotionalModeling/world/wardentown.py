import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Village

class WardenTown(Village):
    """docstring for WardenTown"""
    def __init__(self, **kwargs):
        print(kwargs)
        super().__init__(name="Warden Town", **kwargs)
