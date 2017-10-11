#!python3
import sys, os
sys.path.insert(0, os.path.abspath('..'))
import importlib

places = {
    "Sleepy Hollow" : ("sleepyhollow", "SleepyHollow"),
    "Harvest" : ("harvest", "Harvest"),
    "Fishermans Bay" : ("fishermansbay", "FishermansBay"),
    "Gladesville" : ("gladesville", "Gladesville"),
    "Warden Town" : ("wardentown", "WardenTown"),
    "Northern Plains" : ("northernplains", "NorthernPlains"),
    "Southern Plains" : ("southernplains", "SouthernPlains"),
    "Eastern Plains" : ("easternplains", "EasternPlains"),
    "Western Plains" : ("westernplains", "WesternPlains"),
    "Gloomwood Forest" : ("gloomwoodforest", "GloomwoodForest"),
    "Whitetail Wood" : ("whitetailwood", "WhitetailWood"),
    "Northern Farm" : ("northernfarm", "NorthernFarm"),
    "Southern Farm" : ("southernfarm", "SouthernFarm"),
    "Western Farm" : ("westernfarm", "WesternFarm")
    }

__all__ = [x[0] for x in places.values()]

def getLocation(name):
    if name not in places:
        raise KeyError("Place Name {} does not exist".format(name))
    else:
        M, C = places[name]
        _module = importlib.import_module("world."+M, package=None)
        _class = getattr(_module, C)
        return _class

class WorldMap:
    def __init__(self, logger):
        self.locations = {}
        self.logger = logger.getChild("world")
        self._buildWorld()

    def __contains__(self, item):
        if item in self.locations: return True
        return False

    def __getitem__(self, item):
        if item in self.locations: return self.locations[item]
        raise KeyError("Invalid Location Name")

    def __iter__(self):
        return iter(self.locations.values())

    def addCharacter(self, character, location):
        if location in self.locations:
            self.logger.debug("Adding {} to {}".format(character.name, location))
            self.locations[location].addCharacter(character)
        else:
            raise KeyError("Invalid Location Name")

    def _buildWorld(self):
        self.locations["Warden Town"] = getLocation("Warden Town")(logger=self.logger)
        self.locations["Fishermans Bay"] = getLocation("Fishermans Bay")(logger=self.logger)
        self.locations["Harvest"] = getLocation("Harvest")(logger=self.logger)
        self.locations["Sleepy Hollow"] = getLocation("Sleepy Hollow")(logger=self.logger)
        
        self.locations["Northern Plains"] = getLocation("Northern Plains")(logger=self.logger)
        self.locations["Southern Plains"] = getLocation("Southern Plains")(logger=self.logger)
        self.locations["Eastern Plains"] = getLocation("Eastern Plains")(logger=self.logger)
        self.locations["Western Plains"] = getLocation("Western Plains")(logger=self.logger)

        self.locations["Gloomwood Forest"] = getLocation("Gloomwood Forest")(logger=self.logger)
        self.locations["Whitetail Wood"] = getLocation("Whitetail Wood")(logger=self.logger)

        self.locations["Northern Farm"] = getLocation("Northern Farm")(logger=self.logger)
        self.locations["Southern Farm"] = getLocation("Southern Farm")(logger=self.logger)
        self.locations["Western Farm"] = getLocation("Western Farm")(logger=self.logger)

        # Warden Town
        self.locations["Warden Town"].addLocation("north", self.locations["Northern Plains"])
        self.locations["Warden Town"].addLocation("south", self.locations["Southern Plains"])
        self.locations["Warden Town"].addLocation("east", self.locations["Eastern Plains"])
        self.locations["Warden Town"].addLocation("west", self.locations["Western Plains"])

        # Northern Plains
        self.locations["Northern Plains"].addLocation("north", self.locations["Gloomwood Forest"])
        self.locations["Northern Plains"].addLocation("south", self.locations["Warden Town"])
        self.locations["Northern Plains"].addLocation("east", self.locations["Eastern Plains"])
        self.locations["Northern Plains"].addLocation("west", self.locations["Western Plains"])

        # Southern Plains
        self.locations["Southern Plains"].addLocation("north", self.locations["Warden Town"])
        self.locations["Southern Plains"].addLocation("south", self.locations["Whitetail Wood"])
        self.locations["Southern Plains"].addLocation("east", self.locations["Eastern Plains"])
        self.locations["Southern Plains"].addLocation("west", self.locations["Western Plains"])

        # Eastern Plains
        self.locations["Eastern Plains"].addLocation("north", self.locations["Northern Plains"])
        self.locations["Eastern Plains"].addLocation("south", self.locations["Southern Plains"])
        self.locations["Eastern Plains"].addLocation("east", self.locations["Fishermans Bay"])
        self.locations["Eastern Plains"].addLocation("west", self.locations["Warden Town"])

        # Western Plains
        self.locations["Western Plains"].addLocation("north", self.locations["Northern Plains"])
        self.locations["Western Plains"].addLocation("south", self.locations["Southern Plains"])
        self.locations["Western Plains"].addLocation("east", self.locations["Warden Town"])
        self.locations["Western Plains"].addLocation("west", self.locations["Harvest"])

        # Sleepy Hollow
        self.locations["Sleepy Hollow"].addLocation("north", self.locations["Gloomwood Forest"])
        self.locations["Sleepy Hollow"].addLocation("south", self.locations["Northern Plains"])
        self.locations["Sleepy Hollow"].addLocation("east", self.locations["Gloomwood Forest"])
        self.locations["Sleepy Hollow"].addLocation("west", self.locations["Gloomwood Forest"])

        # Gloomwood Forest
        self.locations["Gloomwood Forest"].addLocation("north", self.locations["Gloomwood Forest"])
        self.locations["Gloomwood Forest"].addLocation("south", self.locations["Sleepy Hollow"])
        self.locations["Gloomwood Forest"].addLocation("east", self.locations["Gloomwood Forest"])
        self.locations["Gloomwood Forest"].addLocation("west", self.locations["Gloomwood Forest"])

        # Whitetail Wood
        self.locations["Whitetail Wood"].addLocation("north", self.locations["Southern Plains"])
        self.locations["Whitetail Wood"].addLocation("south", self.locations["Whitetail Wood"])
        self.locations["Whitetail Wood"].addLocation("east", self.locations["Whitetail Wood"])
        self.locations["Whitetail Wood"].addLocation("west", self.locations["Whitetail Wood"])

        # Fishermans Bay
        self.locations["Fishermans Bay"].addLocation("west", self.locations["Eastern Plains"])

        # Harvest
        self.locations["Harvest"].addLocation("north", self.locations["Northern Farm"])
        self.locations["Harvest"].addLocation("south", self.locations["Southern Farm"])
        self.locations["Harvest"].addLocation("east", self.locations["Western Plains"])
        self.locations["Harvest"].addLocation("west", self.locations["Western Farm"])

        # Farms
        self.locations["Northern Farm"].addLocation("south", self.locations["Harvest"])
        self.locations["Southern Farm"].addLocation("north", self.locations["Harvest"])
        self.locations["Western Farm"].addLocation("east", self.locations["Harvest"])

if __name__ == "__main__":
    test = WorldMap(logger=None)