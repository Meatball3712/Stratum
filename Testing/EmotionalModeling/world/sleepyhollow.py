import sys, os
sys.path.insert(0, os.path.abspath('..'))
from world.biomes import Village

class SleepyHollow(Village):
    """docstring for SleepyHollow"""
    def __init__(self, **kwargs):
        super().__init__(name="Sleepy Hollow", **kwargs)
