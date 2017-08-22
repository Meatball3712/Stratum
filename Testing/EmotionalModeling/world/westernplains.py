import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Plain

class WesternPlains(Plain):
    """docstring for Western Plains"""
    def __init__(self, **kwargs):
        super().__init__(name="Western Plains", **kwargs)
