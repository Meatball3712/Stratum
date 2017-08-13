# ActionObjects Module
import sys, os
sys.path.insert(0, os.path.abspath('..'))
import importlib

__all__ = [
    "attack",
    "eat",
    "givefood",
    "hug",
    "praise",
    "rebuke",
    "run",
    "sleep",
    "talk"
]

# actions = "name" : ("module", "class")
actions = {
    "attack" : ("attack", "Attack"),
    "eat" : ("eat", "Eat"),
    "givefood" : ("givefood", "GiveFood"),
    "hug" : ("hug", "Hug"),
    "praise" : ("praise", "Praise"),
    "rebuke" : ("rebuke", "Rebuke"),
    "run" : ("run", "Run"),
    "sleep" : ("sleep", "Sleep"),
    "talk" : ("talk", "Talk")
}

def getAction(name):
    if name not in actions:
        raise KeyError("Action Name {} does not exist".format(name))
    else:
        M, C = actions[name]
        _module = importlib.import_module("actionObjects."+M, package=None)
        _class = getattr(_module, C)
        return _class

def loadAllActions():
    result = []
    for action in __all__:
        result.append(getAction(action)())
    return result
