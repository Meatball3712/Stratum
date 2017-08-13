import sys, os
sys.path.insert(0, os.path.abspath('..'))
from actionObjects.base import Action
class Dance(Action):
    def __init__(self, **kwargs):
        super().__init__(
            name="dance", 
            desc="{0} dances",
            **kwargs
        )

    def perform(self, source, target, location):
        """
        Ah we can dance if we want to, we can leave your friends behind 
        Cause your friends don't dance and if they don't dance 
        Well they're are no friends of mine 
        """
        # You can only dance when other needs are met.
        if (
                source.stats["hunger"] > 75 and 
                source.stats["health"] == 100 and 
                source.stats["stamina"] > 50 and 
                source.inventory["food"] >= 25 and 
                source.stats["love"] != None and 
                source.stats["love"].love == source
        ):
            self.sourceNeedsDelta["stamina"] = -50
            self.sourceNeedsDelta["dance"] = 10
        
        super().perform(source, target, location)

            