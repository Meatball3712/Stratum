import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Plain

class SouthernPlains(Plain):
    """docstring for Southern Plains"""
    def __init__(self, **kwargs):
        super().__init__(name="Southern Plains", **kwargs)
