import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actions.base import Interaction

class Attack(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="attack", 
            desc="{0} attacks {1}",
            sourceNeedsDelta = {"food":5},
            **kwargs
        )

    def perform(self, source, target, location):
        self.targetNeedsDelta = {"health":-1*source.stats["strength"]}
        return super().perform(source, target, location)