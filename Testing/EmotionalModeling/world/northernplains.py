import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Plain

class NorthernPlains(Plain):
    """docstring for Northern Plains"""
    def __init__(self, **kwargs):
        super().__init__(name="Northern Plains", **kwargs)
