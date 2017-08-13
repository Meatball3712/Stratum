import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Action
class Die(Action):
    def __init__(self, **kwargs):
        super().__init__(
            name="die", 
            desc="And with a final weakly drawn breath {0}'s soul slips into that sweetest of good nights.",
            **kwargs
        )

    def perform(self, source, target, location):
        location.actors.remove(source)
        super().perform(source, target, location)