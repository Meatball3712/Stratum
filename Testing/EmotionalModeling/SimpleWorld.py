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
    
    def __contains__(self, item):
        # Check if actor in location
        if item in self.actors:
            return True
        return False

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

    # All Actions result in an experience.

    def attack(self, intent):
        # Decrease Hunger if monster.
        intent.agent.stamina -= 20
        experience = []
        srcExperience = { "stamina" : -20 }
        trgExperience = {}

        intent.target.health -= intent.agent.strength
        trgExperience["health"] = -1*intent.agent.strength

        if intent.target.health <= 0:
            intent.agent.food += intent.target.food
            srcExperience["food"] = intent.target.food

        return [experience]

    def eat(self, intent):
        if intent.agent.food > 0:
            print(intent)
            intent.agent.food -= 1
            intent.agent.hunger -= 25
            if intent.agent.hunger < 0: intent.agent.hunger = 0
            experience = {
                "hunger" : -25,
                "food" : -1,
            }
            # (intent.agent, action, target, location, experience)
            return [experience]
        else:
            print(intent.agent + " wanted to eat, but had no food")
            return []

    def run(self, intent):
        # You flee takes stamina, but you avoid taking damage
        print(intent)
        intent.agent.stamina -= 20
        return [{"stamina":-20}]

    def zzz(self, intent):
        intent.agent.sleeping -= 1
        intent.agent.stamina += 20
        intent.agent.stamina = 100 if intent.agent.stamina > 100 else intent.agent.stamina
        print(intent)
        return [{"stamina":+20}]

    def sleep(self, intent):
        # Sleep for 5 turns or something
        intent.agent.sleeping = 5
        print(intent)
        return []

    def talk(self, intent):
        # increase friendship rating with one npc.
        if intent.target.sleeping == 0:
            print(intent)
            if intent.target not in self.friends:
                self.friends[intent.target] = 0
            self.friends[intent.target] += 5 # Minor Social improvement
            return [{"belonging":5}]
        else:
            print(intent.agent + "tried to talk to " + intent.target + ", but they were asleep.")
            return []

    def hug(self, intent):
        # You can only hug someone who considers you their love. No cheating.
        if intent.target.love == self and intent.target.sleeping == 0:
            print(intent)
            intent.target.friends[self] += 20 # Big boost to friendliness - reinforces you as their lover.
            return [{"belonging" : 20}]
        elif intent.target.love != self:
            print(intent.agent + " tried to hug " + intent.target + ", but was rejected.")
            # Bad Social Fopar.
            intent.target.friends[self] -= 20 # Unwanted hugs!
            return [{"belonging" : -20}]
        else:
            print(agent + " tried to hug " + intent.target + ", but they were asleep.")
            return []

    def give(self, intent):
        # Maybe in the future.
        if intent.agent.food > 0 and intent.target.sleeping == 0:
            print(intent)
            intent.agent.food -= 1
            intent.target.food += 1
            intent.target.friends[intent.agent.name] = intent.target.friends.get(intent.agent.name, 0) + 10  # Rep Boost
            srcExp = {"food":-1, "belonging":10}
            trgExp = {"food":1}
            return [srcExp, trgExp]
        else:
            print(intent.agent + " tried to give " + intent.target + " some food, but they were asleep")
            return []

    def praise(self, intent):
        # Praise is complicated. The person being praised should feel more esteem. And onlookers will experience different things based on the perspectives of the two involved.
        if intent.target.sleeping == 0 and intent.target in self.actors: # They are local - they can hear it
            print(intent)
            intent.target.respectedBy[intent.agent.name] = intent.target.respectedBy.get(intent.agent.name, 0) + 5
            return [{"esteem" : 5}]
        else:
            print(intent.agent + " praised " + intent.target + " even though they weren't around to hear it")
            return []

    def rebuke(self, intent):
        # Everyone in that location should have an reduced opinion of the target, and a marginal reduced opinion for the source
        if intent.target.sleeping == 0 and intent.target in self.actors: # They are local - they can hear it
            print(intent)
            intent.target.respectedBy[intent.agent.name] = intent.target.respectedBy.get(intent.agent.name, 0) -5
            return [{"esteem" : -5}]
        else:
            print(intent.agent + " praised " + intent.target + " even though they weren't around to hear it")
            return []

    def dance(self, intent):
        """
        Ah we can dance if we want to, we can leave your friends behind 
        Cause your friends don't dance and if they don't dance 
        Well they're are no friends of mine 
        """
        # You can only dance when other needs are met.
        if (
                intent.agent.hunger < 25 and 
                intent.agent.health == 100 and 
                intent.agent.stamina > 50 and 
                intent.agent.food > 0 and 
                intent.agent.love != None and 
                intent.agent.love.target == intent.agent
        ):
            print(intent)
            intent.agent.stamina -= 50
            intent.agent.dance += 1
            experience = {"dance":1, "stamina":-50 }
            return [experience]
        else:
            print(intent.agent + " tried to dance but couldn't get into the swing of things")
            return []

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
    w.addActor(Monster("Grrr"),"forest")
    
    for i in range(5):
        w.update()

