import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Plain

class EasternPlains(Plain):
    """docstring for Eastern Plains"""
    def __init__(self, **kwargs):
        super().__init__(name="Eastern Plains", **kwargs)
