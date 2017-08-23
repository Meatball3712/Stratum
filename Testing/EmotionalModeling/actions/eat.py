import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actions.base import Action
class Eat(Action):
    def __init__(self, **kwargs):
        super().__init__(
            name="eat", 
            desc="{0} eats some food",
            sourceItemDelta = {"food":-1},
            sourceNeedsDelta = {"hunger":5},
            **kwargs
        )