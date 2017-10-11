import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actions.base import Interaction
class GiveFood(Interaction):
    def __init__(self, **kwargs):
        super().__init__(
            name="givefood", 
            desc="{0} gives food to {1}",
            sourceItemDelta = {"food":-1},
            targetItemDelta = {"food":1},
            sourceNeedsDelta = {"friends":1},
            targetNeedsDelta = {"friends":1},
            sourceFeelingsDelta = {"respect":1}, # ? shouldn't the "feeling" be pride
            targetFeelingsDelta = {"respect":1}, # ? shouldn't the "feeling" be gratitude or OCC model
            **kwargs
        )