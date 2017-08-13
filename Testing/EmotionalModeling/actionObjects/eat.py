from base import Action

class Eat(Action):
    """Eating restores hunger. And lets you heal."""
    def __init__(self, name="eat", **kwargs):
        super(Eat, self).__init__(
            name=name, 
            desc="{0} eats some food",
            sourceItemDelta = {"food":-1},
            sourceNeedsDelta = {"hunger":5}
            **kwargs)

        
"""
type: action
name: eat
desc: {0} eats some food
locations:
sourceItemDelta: food|-1
targetItemDelta:
sourceNeedsDelta: hunger|5
targetNeedsDelta:
sourceFeelingsDelta:
targetFeelingsDelta:
locationChange: 0
"""