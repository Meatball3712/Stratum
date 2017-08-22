
import sys, os
sys.path.insert(0, os.path.abspath('..'))
import importlib

races = {
    "Eadrite" : ("eadrite", "Eadrite"),
    "Gloom Stalker" : ("gloom_stalker", "GloomStalker"),
}

__all__ = [x[0] for x in races.values()]

def getRace(name):
    if name not in races:
        raise KeyError("Race Name {} does not exist".format(name))
    else:
        M, C = races[name]
        _module = importlib.import_module("races."+M, package=None)
        _class = getattr(_module, C)
        return _class