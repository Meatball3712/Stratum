import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Interaction
class Talk(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="talk", 
            desc="{0} talks to {1}",
            sourceNeedsDelta = {"friends":5},
            targetNeedsDelta = {"friends":5},
            sourceFeelingsDelta = {"reputation":1},
            targetFeelingsDelta = {"reputation":1},
            **kwargs
        )