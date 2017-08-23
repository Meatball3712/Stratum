import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actions.base import Action
class Sleep(Action):
    def __init__(self, **kwargs):
        super().__init__(
            name="sleep",
            desc="{0} goes to sleep",
            sourceItemDelta = {"stamina":50},
            **kwargs
        )