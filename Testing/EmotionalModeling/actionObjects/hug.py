import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Interaction
class Hug(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="hug",
            desc="{0} hugs {1}",
            **kwargs
        )
        self.lovePower = 5
        self.friendPower = 10

    def perform(self, source, target, location):
        if target.stats["love"] == source:
            self.sourceNeedsDelta = {"love":self.lovePower, "friends":self.friendPower}
            self.targetNeedsDelta = {"love":self.lovePower, "friends":self.friendPower}
        else:
            self.sourceNeedsDelta = {"love":-1*self.lovePower, "friends":-1*self.friendPower}
            self.targetNeedsDelta = {"love":-1*self.lovePower, "friends":-1*self.friendPower}
        super().perform(source, target, location)