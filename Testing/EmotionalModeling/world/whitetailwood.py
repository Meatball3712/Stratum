import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Forest

class WhitetailWood(Forest):
    """docstring for WhitetailWood"""
    def __init__(self, **kwargs):
        super().__init__(name="Whitetail Wood", **kwargs)
