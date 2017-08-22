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

def buildWorld():
    wt = getLocation("Warden Town")()
    fb = getLocation("Fishermans Bay")()
    h = getLocation("Harvest")()
    sh = getLocation("Sleepy Hollow")()
    
    np = getLocation("Northern Plains")()
    sp = getLocation("Southern Plains")()
    ep = getLocation("Eastern Plains")()
    wp = getLocation("Western Plains")()

    gf = getLocation("Gloomwood Forest")()
    ww = getLocation("Whitetail Wood")()

    nf = getLocation("Northern Farm")()
    sf = getLocation("Southern Farm")()
    wf = getLocation("Western Farm")()
    
    # Warden Town
    wt.addLocation("north", np)
    wt.addLocation("south", sp)
    wt.addLocation("east", ep)
    wt.addLocation("west", wp)

    # Northern Plains
    np.addLocation("north", gf)
    np.addLocation("south", wt)
    np.addLocation("east", ep)
    np.addLocation("west", wp)

    # Southern Plains
    sp.addLocation("north", wt)
    sp.addLocation("south", ww)
    sp.addLocation("east", ep)
    sp.addLocation("west", wp)

    # Eastern Plains
    ep.addLocation("north", np)
    ep.addLocation("south", sp)
    ep.addLocation("east", fb)
    ep.addLocation("west", wt)

    # Western Plains
    wp.addLocation("north", np)
    wp.addLocation("south", sp)
    wp.addLocation("east", wt)
    wp.addLocation("west", h)

    # Sleepy Hollow
    sh.addLocation("north", gf)
    sh.addLocation("south", np)
    sh.addLocation("east", gf)
    sh.addLocation("west", gf)

    # Gloomwood Forest
    gf.addLocation("north", gf)
    gf.addLocation("south", sh)
    gf.addLocation("east", gf)
    gf.addLocation("west", gf)

    # Whitetail Wood
    ww.addLocation("north", sp)
    ww.addLocation("south", ww)
    ww.addLocation("east", ww)
    ww.addLocation("west", ww)

    # Fishermans Bay
    fb.addLocation("west", ep)

    # Harvest
    h.addLocation("north", nf)
    h.addLocation("south", sf)
    h.addLocation("east", wp)
    h.addLocation("west", wf)

    # Farms
    nf.addLocation("south", h) # Northern Farm
    sf.addLocation("north", h) # Southern Farm
    wf.addLocation("east", h) # Western Farm

    return wt # Start


def getLocation(name):
    if name not in places:
        raise KeyError("Place Name {} does not exist".format(name))
    else:
        M, C = places[name]
        _module = importlib.import_module("world."+M, package=None)
        _class = getattr(_module, C)
        return _class

if __name__ == "__main__":
    start = buildWorld()