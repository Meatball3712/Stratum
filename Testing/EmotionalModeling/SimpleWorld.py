#SimpleWorld
#for testing agent interaction models
from emotiveAgent import NPC, Monster

class Location:
    """Location Object"""
    def __init__(self, name, description, randomEvents = None):
        self.name = name
        self.directions = {}
        self.actors = []
        self.currentActions = []
        self.logs = []
        self.actorLimit = 10
        #TODO: add a ranodm events system
    
    def isAccessible(self):
        #this can be extended to include lockable doors, etc
        return len(self.actors) < self.actorLimit

    def travel(self, direction, actor):
        #move the actor to another location
        if direction in self.directions and self.directions[direction].isAccessible():
            self.directions[direction].objects.append(actor)
            actor.stamina -= 20
            self.actors.remove(actor)
            #should the actor get tired from moving?
            return actor.name + " moves " + direction + " to " + self.directions[direction].name
        else:
            #maybe make the actor more frustrated?
            pass
    
    def addDirection(self, directionName, location):
        #add an arbitrary direction exit to this location
        self.directions[directionName] = location
    
    def updateActions(self):
        #globally synced step for actors to decide how to act
        #TODO: log intentions
        for actor in self.actors:
            self.currentActions.append(actor.step(self))
            if len(self.currentActions) and len(self.currentActions[-1]):
                logs.append(actor.name + " wants to " + self.currentActions[-1][0].__name__)
    
    def doActions(self):
        #this holds all actions decided for all characters for the global update
        #TODO: log actions and results (and feelings)
        #TODO: update other actors' feelings after actions are performed
        for action in self.currentActions:
            if len(action):
                logs.append(action[0](*action[1:]))
        self.currentActions = []


class World:
    
    def __init__(self, locationData, links):
        #This takes a list of locationnames and descriptions 
        #and a list of {src, dir, dst} triplets which
        #indicate directions through the locations
        self.locations = {}
        for l in locationData:
            print(locations,l)
            self.locations[l["name"]] = Location(l["name"],l["desc"])
        for l in links:
            self.locations[l["src"]].addDirection(l["dir"],self.locations[l["dst"]])
        
        #load actors?
    
    def addActor(self, actor, location):
        self.locations[location].actors.append(actor)
    
    def update(self):
        #TODO: insturment this for collecting logs so we can give actors a customised worldview
        for location in self.locations.items():
            location[1].updateActions()
        
        #now all actors have made choices, they can act
        for location in self.locations.items():
            location[1].doActions()
            print(location[0]+" update Log:")
            for l in location[1].logs:
                print(l)
            print("")
            location[1].logs = []
            


if __name__ == "__main__":
    #NOTE: we could have an ascii coded 2d grid and build larger maps automatically
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
    w = World(locations, locationLinks)
    w.addActor(NPC("Bob"),"village")
    w.addActor(NPC("Alice"),"village")
    w.addActor(NPC("Jim"),"village")
    w.addActor(Monster(100),"forest")
    
    for i in range(5):
        w.update()

