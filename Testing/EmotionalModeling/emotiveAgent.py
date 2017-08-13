# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.

import random
from collections import deque

MaslowHierarchy = {
    "physiology" : 5,
    "security" : 4,
    "belonging" : 3,
    "respect" : 2,
    "self_actualization" : 1
}

class Intention:
    """ Intention Declaration """
    def __init__(self, agent, action, target=None, description=""):
        self.agent = agent
        self.action = action
        self.target = target if target else agent
        self.description = description

    def __str__(self):
        return self.description

    def __repr__(self):
        return "{} -> {} @ {}".format(self.agent, self.action, self.target)

class NPC:
    def __init__(self, name, **kwargs):
        self.name = name
        self.logger = kwargs.get("logger", None)
        self.logger = (self.logger if self.logger else getDefaultLogger).getChild(self.name)

        self.stats = {}
        self.status = {}
        self.inventory = {}

        self.stats["strength"] = kwargs.get("strength", 20) # How hard we attack
        self.stats["hunger"] = kwargs.get("hunger", 100) # Hunger: 100 is sated, 0 is starving
        self.stats["stamina"] = kwargs.get("stamina", 100)
        self.stats["health"] = kwargs.get("health", 100)
        self.stats["friends"] = {}
        self.stats["love"] = None
        self.stats["respectedBy"] = {}
        self.stats["dances"] = 0 # How many dances have we had. We can only dance when all other criteria are satisfied. A measure of fulfillment
        
        self.status["sleeping"] = 0
        self.inventory["food"] = kwargs.get("food", 0)

        self.experience = {} # A dictionary of experiences
    
    def __str__(self):
        return self.name

    def __repr__(self):
        # give us the stats rundown.
        return """{self.name}
------------------
   Health: {self.stats[health]:>5}
   Food:   {self.inventory[food]:>5}
   Stamina:{self.stats[stamina]:>5}
   Hunger: {self.stats[hunger]:>5}
   Friends:{friends:>5}
   Respect:{respect:>5}
   Love:   {love:>5}
   Dances: {self.stats[dances]:>5}
 """.format(self=self, love=(self.stats["love"] if self.stats["love"] else "No One"), friends=sum(list(self.stats["friends"].values())), respect=sum(list(self.stats["respectedBy"].values())))

    def getNeeds(self):
        # Return our current pressing needs out of 100
        result = []
        result.append(("health", (100 - self.health) * MaslowHierarchy["physiology"]))
        result.append(("stamina", (100 - self.stats["stamina"]) * MaslowHierarchy["physiology"]))
        result.append(("hunger", (100 - self.stats["hunger"]) * MaslowHierarchy["physiology"]))
        result.append(("food", (100.0 - self.inventory["food"]) * MaslowHierarchy["security"]))
        result.append(("friends", (100.0 - sum(list(self.stats["friends"].values()))) * MaslowHierarchy["belonging"]))
        result.append(("love", (100-(100 if self.stats["love"] and self.stats["love"].love == self else 50 if self.stats["love"] else 0)) * MaslowHierarchy["belonging"]))
        result.append(("respect", (100.0-sum(list(self.stats["respectedBy"].values()))) * MaslowHierarchy["respect"]))
        result.append(("self_actualization", (100.0-self.stats["dances"]) * MaslowHierarchy["self_actualization"]))
        # Higher the value, higher the need
        return sorted([x for x in result if x[1] > 0], key=lambda x: x[1], reverse=True)
    
    def updateInventory(self, changes, actor, location):
        #TODO: real inv management
        if len(changes) > 0:
            for change, amount in changes.items():
                if (self.inventory.get(change, 0) + amount) < 0:
                    return False

            # Inventory checks out. Perform adjustments
            for change, amount in changes.items():
                self.inventory[change] = self.inventory.get(change, 0) + amount

        return True
    
    def updateFeelings(self, collection, actor, location):
        #TODO: make feelings affect the NPC
        pass
    
    def updateNeeds(self, changes, actor, location):
        #TODO: update needs
        pass
    
    def updateExperience(self, experiences):
        # Update this NPC's experiences
        for intent, location, experience in experiences:
            if isinstance(intent.target, NPC):
                event = (intent.agent.name, intent.action, intent.target.name, location.name)
            else:
                event = (intent.agent.name, intent.action, intent.target, location.name)
            if event not in self.experience:
                self.experience[event] = {}
            for key, value in experience.items():
                if intent.agent.name == self.name: #This was me. Get double XP
                    self.experience[event][key] = self.experience[event].get(key, 0)*0.9 + value*0.2
                else:
                    self.experience[event][key] = self.experience[event].get(key, 0)*0.9 + value*0.1

    def step(self, choices, location):
        return random.choice(choices)
        

        
class Monster(NPC):
    """Monster"""
    def __init__(self, name="Monster", health=20, strength=10, food=25, **kwargs):
        NPC.__init__(self, name, health=health, strength=strength, food=food, **kwargs)
        self.health = health # If we want to have varying difficulty monsters
        self.shitList = []
        self.aggression = 0.25
    
    def step(self, choices, location):
        # If someone interacted with it, and they're still around. Attack them.
        print(choices)
        for c in choices:
            if c[0].name == "attack":
                if c[2] in self.shitList:
                    return c
                elif random.random() < self.aggression and c[2] is not self:
                    self.shitList.append(c[2])
                    return c
        #else sleep
        for c in choices:
            if c[0].name == "sleep":
                return c

    def updateExperiences(self, experiences):
        for intent, location, experience in experiences:
            if intent.target == self:
                # You made my list.
                if intent.action == "attack":
                    #You attacked me!?
                    self.shitList.append((intent.agent, 2))
                else:
                    # You dare disturb me!?
                    self.shitList.append((intent.agent, 1))
