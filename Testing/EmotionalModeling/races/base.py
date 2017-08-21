# Character
from emotionalModel import Personality
# from AI import TDModel
# from AI import QModel

class Character(Personality):
    """ Model of a generic NPC """
    def __init__(self, name, bio="", **kwargs):
        self.name = name
        self.bio = bio
        self.TDModel = kwargs.get("TDModel", None)
        self.QModel = kwargs.get("QModel", None)

        self.stats = {}
        self.stats["strength"] = (kwargs.get("strength", 20), 19, 1, "weakened", "collapse"),  # How hard we attack, when diminished causes feeling of weak
        self.stats["hunger"] = (kwargs.get("hunger", 100), 50, 2, "hungry", "drain") # Hunger: 100 is sated, 0 is starving, when diminished causes feeling for hungry. When depleted drains health and stamina
        self.stats["stamina"] = (kwargs.get("stamina", 100), 50, 1, "exhausted", "collapse") # When diminished causes feeling of exhausted
        self.stats["health"] = (kwargs.get("health", 100), 90, 1.5, "pain", "die")  # When diminished causes feeling of pain

        self.inventory = {
            "food" : 0
        }

        # Additional bits. Empathy? How much we consider otherpeoples consequences
        Personality.__init__(self, TModel=self.TDModel, QModel=self.QModel, kwargs.get("mood", (0,0,0)), empathy=1.0)

    def __str__(self):
        return self.name

    def __repr__(self):
        # give us the stats rundown.
        return """{self.name}
------------------
   Health: {health:>5}
   Food:   {self.inventory[food]:>5}
   Stamina:{stamina:>5}
   Hunger: {hunger:>5}
""".format(
        self,
        health=self.stats["health"][0],
        stamina=self.stats["stamina"][0]
    )

    def getVector(self, introspective=True):
        """
        Return a numpy array with every stat in order.
        """
        status = np.zeros((7,))
        # Format:
        # --------

        if introspective:
            status[0] = self.personality.mood[0]    # Mood: P
            status[1] = self.personality.mood[1]    # Mood: A
            status[2] = self.personality.mood[2]    # Mood: D

            status[4] = self.stat["stamina"]        # Stat: stamina
            status[5] = self.stat["hunger"]         # Stat: hunger
            status[6] = self.stat["strength"]       # Stat: strength

        status[3] = self.stat["health"]             # Stat: Health

        return status

class Monster(Personality):
    def __init__(self, name, bio="", **kwargs):
        self.name = name
        self.bio = bio
        self.TDModel = kwargs.get("TDModel", None)
        self.QModel = kwargs.get("QModel", None)

        self.stats = {}
        self.stats["strength"] = (kwargs.get("strength", 20), 19, 1, "weakened", "collapse"),  # How hard we attack, when diminished causes feeling of weak
        self.stats["hunger"] = (kwargs.get("hunger", 100), 50, 2, "hungry", "drain") # Hunger: 100 is sated, 0 is starving, when diminished causes feeling for hungry. When depleted drains health and stamina
        self.stats["stamina"] = (kwargs.get("stamina", 100), 50, 1, "exhausted", "collapse") # When diminished causes feeling of exhausted
        self.stats["health"] = (kwargs.get("health", 100), 90, 1.5, "pain", "die")  # When diminished causes feeling of pain

        self.inventory = {
            "food" : 25
        }

        Personality.__init__(self, TModel=self.TDModel, QModel=self.QModel, kwargs.get("mood", (-0.5,0.5,0.5)), empathy=0.0) # Start Aggressive

    def __str__(self):
        return self.name

    def __repr__(self):
        # give us the stats rundown.
        return """{self.name}
------------------
   Health: {health:>5}
   Food:   {self.inventory[food]:>5}
   Stamina:{stamina:>5}
   Hunger: {hunger:>5}
""".format(
        self,
        health=self.stats["health"][0],
        stamina=self.stats["stamina"][0]
    )

    def getVector(self, introspective=True):
        """
        Return a numpy array with every stat in order.
        """
        status = np.zeros((7,))
        # Format:
        # --------

        if introspective:
            status[0] = self.personality.mood[0]    # Mood: P
            status[1] = self.personality.mood[1]    # Mood: A
            status[2] = self.personality.mood[2]    # Mood: D

            status[4] = self.stat["stamina"]        # Stat: stamina
            status[5] = self.stat["hunger"]         # Stat: hunger
            status[6] = self.stat["strength"]       # Stat: strength


        status[3] = self.stat["health"]             # Stat: Health

        return status