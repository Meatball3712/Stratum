import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Interaction
class Praise(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="praise",
            desc="{0} praises {1}",
            sourceNeedsDelta = {"friends" : 1},
            targetNeedsDelta = {"friends" : 1},
            sourceFeelingsDelta = {"respect" : 5},
            targetFeelingsDelta = {"respect" : 5},
            **kwargs
        )