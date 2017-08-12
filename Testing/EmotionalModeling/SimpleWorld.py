#SimpleWorld
#for testing agent interaction models
from emotiveAgent import NPC, Monster
import logging
from logging.handlers import RotatingFileHandler
import time

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

class Location:
    """Location Object"""
    def __init__(self, name, description, randomEvents = None, **kwargs):
        self.name = name
        self.directions = {}
        self.actors = []
        self.currentActions = []
        self.currentExperiences = []
        self.logs = []
        self.actorLimit = 10
        self.logger = kwargs.get("logger", None)
        self.logger = (self.logger if self.logger else setupDefaultLogger()).getChild(self.name)

        #TODO: add a random events system
        self.actionMap = {
            "travel" : self.travel,
            "attack" : self.attack,
            "sleep" : self.sleep,
            "run" : self.run,
            "eat" : self.eat,
            "talk" : self.talk,
            "hug" : self.hug,
            "praise" : self.praise,
            "rebuke" : self.rebuke,
            "give" : self.give,
            "dance" : self.dance
        }
    
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
        if agent.stamina < 80: actions += ["sleep"]
        if agent.food >= 25 and len(self.actors) > 1: actions += ["give"]
        if agent.food >= 25: actions += ["eat"]
        if agent.stamina > 20 and len(self.actors) > 1: actions += ["attack"]
        if agent.stamina > 20: actions += ["travel"]
        if len(self.actors)>1: actions += ["talk", "praise", "rebuke"]
        if agent.love in self.actors: actions += ["hug"]
        if (
                agent.hunger > 75 and 
                agent.health == 100 and 
                agent.stamina > 50 and 
                agent.food >= 25 and 
                agent.love != None and 
                agent.love.target == agent
        ): actions += ["dance"]
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
            intention = actor.step(self)
            if intention: 
                self.logger.debug(repr(intention))
                self.currentActions.append(intention)
                
    
    def doActions(self):
        #this holds all actions decided for all characters for the global update
        #TODO: log actions and results (and feelings)
        #TODO: update other actors' feelings after actions are performed
        self.experience = []
        for intent in self.currentActions:
            if intent.action in self.actionMap:
                exp = self.actionMap[intent.action](intent)
                if exp:
                    self.experience.append((intent, self, exp))

    def shareExperiences(self):
        for actor in self.actors:
            actor.updateExperience(self.experience)

    def travel(self, intent):
        #move the actor to another location
        if intent.target in self.directions and self.directions[intent.target].isAccessible():
            self.logger.info("{} and arrives at {}".format(intent, self.directions[intent.target].name))
            self.directions[intent.target].actors.append(intent.agent)
            intent.agent.stamina -= 20
            self.actors.remove(intent.agent)
            #should the actor get tired from moving?
            return {"stamina":-20}
        else:
            #maybe make the actor more frustrated?
            self.logger.info("{} tries to head {} but their way is blocked".format(intent.agent, intent.target))
            return None

    def attack(self, intent):
        # Decrease Hunger if monster.
        self.logger.info(intent)
        intent.agent.stamina -= 20
        experience = []
        srcExperience = { "stamina" : -20 }
        trgExperience = {}

        intent.target.sleeping = 0  # You're not sleeping through this
        intent.target.health -= intent.agent.strength
        trgExperience["health"] = -1*intent.agent.strength

        if intent.target.health <= 0:
            intent.agent.food += intent.target.food
            srcExperience["food"] = intent.target.food

        return experience

    def eat(self, intent):
        if intent.agent.food > 25:
            self.logger.info(intent)
            intent.agent.food -= 25
            intent.agent.hunger += 25
            if intent.agent.hunger > 100: intent.agent.hunger = 100
            experience = {
                "hunger" : +25,
                "food" : -25,
            }
            # (intent.agent, action, target, location, experience)
            return experience
        else:
            self.logger.info("{} wanted to eat, but had no food".format(intent.agent))
            return None

    def run(self, intent):
        # You flee takes stamina, but you avoid taking damage
        self.logger.info(intent)
        intent.agent.stamina -= 20
        return {"stamina":-20}

    def sleep(self, intent):
        # Sleep for 5 turns or something
        if intent.agent.sleeping == 0:
            intent.agent.sleeping = 2
        
        intent.agent.sleeping -= 1
        intent.agent.stamina += 20
        if intent.agent.stamina >= 100: # Wake up.
            intent.agent.stamina == 100
            intent.agent.sleeping=0
         
        self.logger.info(intent)
        return {"stamina":+20}

    def talk(self, intent):
        # increase friendship rating with one npc.
        if intent.target.sleeping == 0:
            self.logger.info(intent)
            if intent.target not in intent.agent.friends:
                intent.agent.friends[intent.target] = 0
            intent.agent.friends[intent.target] += 5 # Minor Social improvement
            return {"friends":5}
        else:
            self.logger.info("{} tried to talk to {}, but they were asleep.".format(intent.agent, intent.target))
            return None

    def hug(self, intent):
        # You can only hug someone who considers you their love. No cheating.
        if intent.target.love == self and intent.target.sleeping == 0:
            self.logger.info(intent)
            intent.target.friends[intent.agent.name] =  intent.target.friends.get(intent.agent.name, 0) + 20 # Big boost to friendliness - reinforces you as their lover.
            return {"friends" : 20, "love":100}
        elif intent.target.love != intent.agent:
            self.logger.info("{} tried to hug {}, but was rejected.".format(intent.agent, intent.target))
            # Bad Social Fopar.
            intent.target.friends[intent.agent.name] = intent.target.friends.get(intent.agent.name, 0) - 20 # Unwanted hugs!
            return {"friends" : -20}
        else:
            self.logger.info("{} tried to hug {}, but they were asleep.".format(intent.agent, intent.target))
            return None

    def give(self, intent):
        # Maybe in the future.
        if intent.agent.food >= 25 and intent.target.sleeping == 0:
            self.logger.info(intent)
            intent.agent.food -= 25
            intent.target.food += 25
            intent.target.friends[intent.agent.name] = intent.target.friends.get(intent.agent.name, 0) + 10  # Rep Boost
            srcExp = {"food":-25, "friends":10}
            #trgExp = {"food":25} # Irrelevant what the target gets. We only care about what the giver gets.
            return srcExp
        else:
            self.logger.info("{} tried to give {} some food, but they were asleep".format(intent.agent, intent.target))
            return None

    def praise(self, intent):
        # Praise is complicated. The person being praised should feel more respect. And onlookers will experience different things based on the perspectives of the two involved.
        if intent.target.sleeping == 0 and intent.target in self.actors: # They are local - they can hear it
            self.logger.info(intent)
            intent.target.respectedBy[intent.agent.name] = intent.target.respectedBy.get(intent.agent.name, 0) + 5
            return {"respect" : 5}
        else:
            self.logger.info("{} praised {} even though they weren't able to hear it".format(intent.agent, intent.target))
            return None

    def rebuke(self, intent):
        # Everyone in that location should have an reduced opinion of the target, and a marginal reduced opinion for the source
        if intent.target.sleeping == 0 and intent.target in self.actors: # They are local - they can hear it
            self.logger.info(intent)
            intent.target.respectedBy[intent.agent.name] = intent.target.respectedBy.get(intent.agent.name, 0) -5
            return {"respect" : -5}
        else:
            self.logger.info("{} praised {} even though they weren't able to hear it".format(intent.agent, intent.target))
            return None

    def die(self, intent):
        # Rest in Peace - this is complicated?
        self.actors.remove(intent.agent)
        return None

    def dance(self, intent):
        """
        Ah we can dance if we want to, we can leave your friends behind 
        Cause your friends don't dance and if they don't dance 
        Well they're are no friends of mine 
        """
        # You can only dance when other needs are met.
        if (
                intent.agent.hunger > 75 and 
                intent.agent.health == 100 and 
                intent.agent.stamina > 50 and 
                intent.agent.food >= 25 and 
                intent.agent.love != None and 
                intent.agent.love.target == intent.agent
        ):
            self.logger.info(intent)
            intent.agent.stamina -= 50
            intent.agent.dance += 10
            experience = {"self_actualisation":10, "stamina":-50 }
            return experience
        else:
            self.logger.info(intent.agent + " tried to dance but couldn't get into the swing of things")
            return None

class World:
    
    def __init__(self, locationData, links, logger=None):
        #This takes a list of locationnames and descriptions 
        #and a list of {src, dir, dst} triplets which
        #indicate directions through the locations
        self.logger = logger if logger else setupDefaultLogger()
        self.locations = {}
        self.cast = []
        for l in locationData:
            self.logger.debug("Creating Location {name}: {desc}".format(**l))
            self.locations[l["name"]] = Location(l["name"],l["desc"],logger=self.logger)
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
    w = World(locations, locationLinks, logger=logger)
    w.addActor(NPC("Bob",logger=logger),"village")
    w.addActor(NPC("Alice",logger=logger),"village")
    w.addActor(NPC("Jim",logger=logger),"village")
    w.addActor(Monster("The Dread Seeker",logger=logger),"forest")
    
    c = 0
    while c < 5 and len([x for x in w.cast if (not isinstance(x, Monster) and x.health>0)]):
        for i in range(20):
            w.update()
        for actor in w.cast:
            print(repr(actor))
        c += 1
    if c == 5:
        logger.info("End Simulation")
    else:
        logger.error("Uhoh - Everyone's dead.")


