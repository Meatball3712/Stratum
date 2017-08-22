# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.

import random, csv
from collections import deque
from emotionalModel import Personality, PersonalView, PersonalExperience
import numpy as np

MaslowHierarchy = {
    "physiology" : 5,
    "security" : 4,
    "belonging" : 3,
    "respect" : 2,
    "self_actualization" : 1
}



class NPC:
    def __init__(self, name, **kwargs):
        self.name = name
        self.logger = kwargs.get("logger", None)
        self.logger = (self.logger if self.logger else getDefaultLogger).getChild(self.name)
        self.world = kwargs.get("world", None)
        self.race = kwargs.get("race", "Eadrite")

        # These aren't feelings. They're physical states the evoke feelings based on their condition. Normally a negative feeling of pain as they get low. 
        # Stats[stat] = (max, threshold, multiplier, feeling, compel)
        self.stats = {} # Our Physical Stats.
        self.stats["strength"] = (kwargs.get("strength", 20), 19, 1, "weakened", "collapse"),  # How hard we attack, when diminished causes feeling of weak
        self.stats["hunger"] = (kwargs.get("hunger", 100), 50, 2, "hungry", "collapse") # Hunger: 100 is sated, 0 is starving, when diminished causes feeling for hungry
        self.stats["stamina"] = (kwargs.get("stamina", 100), 50, 1, "exhausted", "collapse") # When diminished causes feeling of exhausted
        self.stats["health"] = (kwargs.get("health", 100), 90, 1.5, "pain", "die")  # When diminished causes feeling of pain

        self.status = {} # For status effects that affect our body and mind. E.g. Asleep, Collapsed, Dead. These are game mechanics.

        self.inventory = {}
        self.inventory["food"] = kwargs.get("food", 0)

        # Personal Views
        self.worldView = PersonalView(loadFile="worldView.csv")
        self.individualView = PersonalView(loadFile=None) # New blank individual view
        self.personality = Personality(worldView=self.worldView, individualView = self.individualView)


        # These aren't stats.
        self.stats["friends"] = {} # Moved to individualView under personality.
        self.stats["love"] = None # This is way to simple. 
        self.stats["respectedBy"] = {}
        self.stats["dances"] = 0 # How many dances have we had. We can only dance when all other criteria are satisfied. A measure of fulfillment

        self.goals = [] # Current plan is goal[0]
        # Sleeping etc should be compelled actions caused by the body. As well as desires to counter a state.

        # Initialise Experience Model
        # self.experience = PersonalExperience(self.worldView, self.individualView, loadFile="innateExperience.json")


        # with open("innateExperience.csv", "r") as f:
        #     reader = csv.reader(f)
        #     header = next(reader, None)
        #     for row in reader:
        #         if source not in
    
    def __str__(self):
        return self.name

    def __repr__(self):
        # give us the stats rundown.
        return """{self.name}
------------------
   Health: {health:>5}
   Food:   {self.inventory[food]:>5}
   Stamina:{stamina:>5}
   Hunger: {hunger:>5}
 """.format(
        self,
        health=self.stats["health"][0],
        stamina=self.stats["stamina"][0]
    )

    def getVector(self, introspective=True):
        """
        Return a numpy array with every stat in order.
        """
        status = np.zeros((6,))
        # Format:
        # --------

        if introspective:
            status[0] = self.personality.mood[0]    # Mood: P
            status[1] = self.personality.mood[1]    # Mood: A
            status[2] = self.personality.mood[2]    # Mood: D

            status[4] = self.stat["stamina"]        # Stat: stamina
            status[5] = self.stat["hunger"]         # Stat: hunger

        status[3] = self.stat["health"]             # Stat: Health

        return status
        

    def getNeeds(self):
        # Return our current pressing needs out of 100 
        # Don't like!!! need to get needs based on sum total of our current environmental variables. Also need to identify sources of grievences.
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

class GloomStalker(Monster):
    pass

class Eadrite(NPC):
    pass