#SimpleWorld
#for testing agent interaction models
from emotiveAgent import NPC, Monster
import logging
import os
from logging.handlers import RotatingFileHandler
import time
import actionObjects

def setupDefaultLogging(debug=False):
    # Setup Default Logging
    logger = logging.getLogger("SimpleWorld")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    h = logging.StreamHandler()
    h.setLevel(logging.DEBUG)
    h.setFormatter(fmt)
    logger.addHandler(h)

    fmt = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    h = RotatingFileHandler("EMTesting.log", maxBytes=1000000, backupCount=5)
    h.setLevel(logging.INFO)
    h.setFormatter(fmt)
    logger.addHandler(h)

    return logger

# DEPRECATED - Moved to Actions Module
"""
def loadAction(fname):
    # load line entries
    print(fname)
    entries = {}
    for l in open(fname,'r').readlines():
        v = l.split(':')
        if len(v) > 1:
            entries[v[0].strip(' \r\n')] = v[1].strip(' \r\n')
        else:
            entries[v[0].strip(' \r\n')] = ""
    #split collections
    entries["locations"] = [r.strip(' \r\n') for r in entries["locations"].split(' ')] if len(entries["locations"]) else []
    entries["sourceItemDelta"] = [r.split('|') for r in entries["sourceItemDelta"].split(' ')] if len(entries["sourceItemDelta"]) else []
    entries["targetItemDelta"] = [r.split('|') for r in entries["targetItemDelta"].split(' ')] if len(entries["targetItemDelta"]) else []
    entries["sourceNeedsDelta"] = [r.split('|') for r in entries["sourceNeedsDelta"].split(' ')] if len(entries["sourceNeedsDelta"]) else []
    entries["targetNeedsDelta"] = [r.split('|') for r in entries["targetNeedsDelta"].split(' ')] if len(entries["targetNeedsDelta"]) else []
    entries["sourceFeelingsDelta"] = [r.split('|') for r in entries["sourceFeelingsDelta"].split(' ')] if len(entries["sourceFeelingsDelta"]) else []
    entries["targetFeelingsDelta"] = [r.split('|') for r in entries["targetFeelingsDelta"].split(' ')] if len(entries["targetFeelingsDelta"]) else []
    
    return Action(entries["name"],
                  entries["type"],
                  entries["desc"],
                  entries["locations"],
                  entries["sourceItemDelta"],
                  entries["targetItemDelta"],
                  entries["sourceNeedsDelta"],
                  entries["targetNeedsDelta"],
                  entries["sourceFeelingsDelta"],
                  entries["targetFeelingsDelta"],
                  int(entries["locationChange"]))

class Action:
    
    def __init__(self, 
                 name,
                 mytype, 
                 desc,
                 availableLocations,
                 itemDelta,
                 targetItemDelta,
                 sourceNeedsDelta,
                 targetNeedsDelta,
                 sourceFeelingsDelta,
                 targetFeelingsDelta,
                 locationChange = False):
        #TODO: add stat modifiers to values and durations to actions
        self.name = name
        self.type = mytype
        self.desc = desc
        self.locations = availableLocations
        self.itemDelta = itemDelta
        self.targetItemDelta = targetItemDelta
        self.needsDelta = sourceNeedsDelta
        self.targetNeedsDelta = targetNeedsDelta
        self.feelingsDelta = sourceFeelingsDelta
        self.targetFeelingsDelta = targetFeelingsDelta
        self.locationChange = locationChange
    
    def perform(self, source, target, location):
        print(target)
        if source.updateInventory(self.itemDelta, target, location):
            print(self.name,self.locationChange)
            if self.locationChange:
                if location.directions[target].isAccessible():
                    location.directions[target].actors.append(source)
                    location.actors.remove(source)
                    source.updateNeeds(self.needsDelta, target, location)
                else:
                    return "{0} cannot be performed by {1} towards {2}".format(self.name,source.name,target)
            elif target != None:
                if target.updateInventory(self.targetItemDelta, source, location): 
                    #if we have a non-direction target, it's an actor
                    #TODO: check if the target is sleeping
                    source.updateFeelings(self.feelingsDelta, target, location)
                    source.updateNeeds(self.needsDelta, target, location)
                    target.updateFeelings(self.targetFeelingsDelta, source, location)
                    target.updateNeeds(self.targetNeedsDelta, source, location)
                    return self.desc.format(source.name, target.name, location.name)
                else:
                    return "{0} cannot be performed by {1} on {2}".format(self.name,source.name,target.name)
            else:
                source.updateFeelings(self.feelingsDelta, target, location)
                source.updateNeeds(self.needsDelta, target, location)
            return self.desc.format(source.name, target, location.name)
        return "{0} cannot be performed by {1} due to insufficient inventory".format(self.name,source.name)
"""

class Location:
    """Location Object"""
    def __init__(self, name, description, actions, randomEvents = None, **kwargs):
        self.name = name
        self.directions = {}
        self.actors = []
        #we should change this to test if location is of the right type
        print(actions)
        self.actions = {a.name:a for a in actions if len(a.locations) == 0 or name in a.locations}
        self.currentActions = []
        self.currentExperiences = []
        self.logs = []
        self.actorLimit = 10
        self.logger = kwargs.get("logger", None)
        self.logger = (self.logger if self.logger else setupDefaultLogger()).getChild(self.name)

        #TODO: add a random events system
    
    def __contains__(self, item):
        # Check if actor in location
        if isinstance(item, NPC) and item in self.actors:
            return True
        elif isinstance(item, str) and item in [x.name for x in self.actors]:
            return True
        else:
            return False

    def availableActions(self, agent):
        actions = []
        
        for k,a in self.actions.items():
            print(a.name)
            #if we are a move action, append all valid directions
            if isinstance(a, actionObjects.base.Movement) :
                for d, l in self.directions.items():
                    print(d)
                    actions.append([a,agent,d,self])
            #if we are an interaction, append all valid actors
            elif isinstance(a, actionObjects.base.Interaction):
                for t in self.actors:
                    if t is not agent:
                        actions.append([a,agent,t,self])
            #if we are an action (no target), simply append
            elif isinstance(a, actionObjects.base.Action):
                actions.append([a,agent,None,self])
        print(actions)
        return actions

    def isAccessible(self):
        #this can be extended to include lockable doors, etc
        return len(self.actors) < self.actorLimit
    
    def getActor(self, name):
        for a in self.actors:
            if a.name == name:
                return a
        return None

    def addDirection(self, directionName, location):
        #add an arbitrary direction exit to this location
        self.directions[directionName] = location
    
    def updateActions(self):
        #globally synced step for actors to decide how to act
        self.currentActions = []
        for actor in self.actors:
            intention = actor.step(self.availableActions(actor),self)
            if intention: 
                self.logger.debug(repr(intention))
                self.currentActions.append(intention)
                
    
    def doActions(self):
        #this holds all actions decided for all characters for the global update
        #TODO: log actions and results (and feelings)
        #TODO: update other actors' feelings after actions are performed
        self.experience = []
        for intent in self.currentActions:
            print(intent[0].perform(*intent[1:]))
            #TODO: annotate experience in some way
            exp = None
            if exp:
                self.experience.append((intent, self, exp))

    def shareExperiences(self):
        for actor in self.actors:
            actor.updateExperience(self.experience)

class World:
    
    def __init__(self, locationData, links, actions, logger=None):
        #This takes a list of locationnames and descriptions 
        #and a list of {src, dir, dst} triplets which
        #indicate directions through the locations
        self.actions = actions
        self.logger = logger if logger else setupDefaultLogger()
        self.locations = {}
        self.cast = []
        for l in locationData:
            self.logger.debug("Creating Location {name}: {desc}".format(**l))
            self.locations[l["name"]] = Location(l["name"],l["desc"],self.actions,logger=self.logger)
        for l in links:
            self.locations[l["src"]].addDirection(l["dir"],self.locations[l["dst"]])
        
        #load actors?
    
    def addActor(self, actor, location):
        self.cast.append(actor)
        self.locations[location].actors.append(actor)
    
    def update(self):
        #TODO: insturment this for collecting logs so we can give actors a customised worldview
        print()
        self.logger.debug("--- Collect Intentions ---")
        for location in self.locations.values():
            location.updateActions()
        
        #now all actors have made choices, they can act
        self.logger.debug("--- Execute Intentions ---")
        for location in self.locations.values():
            location.doActions()

        self.logger.debug("--- Sharing Experiences ---")
        for location in self.locations.values():
            location.shareExperiences()
        
        time.sleep(0)


if __name__ == "__main__":
    #NOTE: we could have an ascii coded 2d grid and build larger maps automatically
    logger = setupDefaultLogging()

    from actionObjects import attack

    #######
    # P f #
    # V F #
    #######
    locations = ({"name":"village","desc":"a colourful village"},
                 {"name":"farms","desc":"farmlands near the village"},
                 {"name":"plains","desc":"open grassy plains"},
                 {"name":"forest","desc":"dark gloomy forest"})
    locationLinks = ({"src":"village","dst":"plains","dir":"North"},
                     {"src":"plains","dst":"village","dir":"South"},
                     {"src":"farms","dst":"forest","dir":"North"},
                     {"src":"forest","dst":"farms","dir":"South"},
                     {"src":"village","dst":"farms","dir":"East"},
                     {"src":"farms","dst":"village","dir":"West"},
                     {"src":"plains","dst":"forest","dir":"East"},
                     {"src":"forest","dst":"plains","dir":"West"})
    actions = actionObjects.loadAllActions()
    w = World(locations, locationLinks, actions, logger=logger)
    w.addActor(NPC("Bob",logger=logger),"village")
    w.addActor(NPC("Alice",logger=logger),"village")
    w.addActor(NPC("Jim",logger=logger),"village")
    w.addActor(Monster("The Dread Seeker",logger=logger),"forest")
    
    
    
    c = 0
    while c < 5 and len([x for x in w.cast if (not isinstance(x, Monster) and x.stats["health"]>0)]):
        for i in range(1):
            w.update()
        for actor in w.cast:
            print(repr(actor))
        c += 1
    if c == 5:
        logger.info("End Simulation")
    else:
        logger.error("Uhoh - Everyone's dead.")


