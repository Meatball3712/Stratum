# All the world Biomes
import sys, os
sys.path.insert(0, os.path.abspath('..'))

class Biome():
    """Base Biome Class"""
    def __init__(self, name, logger, **kwargs):
        # Name
        self.name = name
        self.description = kwargs.get("description", "")
        self.logger = logger

        # Directions
        self.north = kwargs.get("north", None)
        self.south = kwargs.get("south", None)
        self.east = kwargs.get("east", None)
        self.west = kwargs.get("west", None)

        # Characters
        self.characters = []


    def addLocation(self, direction, place):
        assert isinstance(place, Biome)
        if direction not in ("north","south","east","west"):
            raise KeyError("Invalid Direction {}".format(direction))
        elif direction == "north": self.north = place
        elif direction == "south": self.south = place
        elif direction == "east": self.east = place
        else: self.west = place

    def addCharacter(self, character):
        self.characters.append(character)


class Farm(Biome):
    """Farm Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
class Plain(Biome):
    """Plain Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

class Forest(Biome):
    """Forest Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
class Village(Biome):
    """Village Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)