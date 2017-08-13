import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Movement
class Run(Movement):
    def __init__(self, **kwargs):
        super().__init__(
            name="run",
            desc="{0} runs away",
            sourceItemDelta = {"stamina":-20},
            locationChange = 1,
            **kwargs
        )