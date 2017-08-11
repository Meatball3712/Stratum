# Character
from emotionalModel import Personality

class Character(Personality):
    """ Model of an NPC """
    def __init__(self, name, bio="", **kwargs):
        Personality.__init__(self, kwargs.get("mood", (0,0,0)))
        self.name = name
        self.surname = kwargs.get("surname", "")
        self.bio = bio
        