import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Interaction
class Rebuke(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="rebuke",
            desc="{0} rebukes {1}",
            sourceNeedsDelta = {"friends" : -1},
            targetNeedsDelta = {"friends" : -1},
            sourceFeelingsDelta = {"respect" : -5},
            targetFeelingsDelta = {"respect" : -5},
            **kwargs
        )