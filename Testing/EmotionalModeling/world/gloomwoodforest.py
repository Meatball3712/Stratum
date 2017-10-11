import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Forest

class GloomwoodForest(Forest):
    """docstring for GloomwoodForest"""
    def __init__(self, **kwargs):
        super().__init__(name="Gloomwood Forest", **kwargs)
