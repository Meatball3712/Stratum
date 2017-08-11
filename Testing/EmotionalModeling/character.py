# Character
from emotionalModel import Personality

class Character(Personality):
    """ Model of an NPC """
    def __init__(self, name, surname=""):
        self.name = name
        self.surname = surname