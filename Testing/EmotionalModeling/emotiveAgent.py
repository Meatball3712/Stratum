# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.

import random
from collections import deque

MaslowHierarchy = {
    "physiology" : 5,
    "security" : 4,
    "belonging" : 3,
    "esteem" : 2,
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

         # Set goals based on Heirarchy of needs?
        self.sleeping = 0
        self.strength = kwargs.get("strength", 20) # How hard we attack
        self.food = kwargs.get("food", 0)
        
        # Physiology - Food/Water/Breathing etc. (May not be relevent unless we want to make a survival game)
        self.hunger = kwargs.get("hunger", 0)
        self.stamina = kwargs.get("stamina", 100)

        # Safety - Security of body, family, health, resources
        self.health = kwargs.get("health", 100)

        # Love/Belonging - Friendship/Family/Intimacy
        self.belonging = 0 # How many people call me friend. Do I love anyone
        self.friends = {}
        self.love = None
        self.rivals = {}
        # Talking with someone increases friendliness, as does recieving praise
        # unless that person is a rival love interest (relative friendliness to our prospective mate)

        # Esteem - Confidence, Achievement, respect of and by others.
        # Earned by offering and recieving praise, deminished by rebukes
        self.respectedBy = {}
        self.respectForOthers = {}

        # Self-Actualisation: Morality, Creativity, Spontaneity, problem solving, lack of prejudice acceptance of facts (How to model this!?)
        self.dances = 0 # How many dances have we had. We can only dance when all other criteria are satisfied. A measure of fulfillment

        self.actions = {
            "sleep" : self.sleep,
            "zzz" : self.zzz,
            "attack" : self.attack,
            "run" : self.run,
            "eat" : self.eat,
            "travel" : self.travel,
            "talk" : self.talk,
            "hug" : self.hug,
            "praise" : self.praise,
            "rebuke" : self.rebuke,
            "give" : self.give,
            "dance" : self.dance
        }

        self.experience = {} # A dictionary of experiences
        # (source, action, target, location) = (change in stats)
    
    def __str__(self):
        return self.name

    def getMaslowHierarchy(self):
        # Return our current pressing needs out of 100
        result = []
        result.append(("physiology", ((100-(self.health + self.stamina) / 2)) * MaslowHierarchy["physiology"]))
        result.append(("security", (100-(100.0*self.food/4)) * MaslowHierarchy["security"]))
        result.append(("belonging", (100.0-((sum(list(self.friends.values())) + (25.0 if self.love else 0.0)))) * MaslowHierarchy["belonging"]))
        result.append(("esteem", (100.0-(sum(list(self.respectedBy.values())))) * MaslowHierarchy["esteem"]))
        result.append(("self_actualization", (100.0-(self.dances/10.0)) * MaslowHierarchy["self_actualization"]))
        # Higher the value, higher the need
        return sorted(result, key=lambda x: x[1])


    def travel(self, direction):
        #TODO: change this whole thing to use the travel attached to the location
        return Intention(self, "travel", direction, self.name + " travels " + direction)

    def attack(self, target):
        return Intention(self, "attack", target, self.name + " attacks " + target.name)

    def eat(self):
        return Intention(self, "eat", description=self.name + " eats some food")

    def run(self):
        return Intention(self, "run", description=self.name + " runs away")

    def zzz(self):
        return Intention(self, "zzz", description = self.name + " sleeps")

    def sleep(self):
        return Intention(self, "sleep", description = self.name + " goes to sleep")

    def talk(self, target):
        return Intention(self, "talk", target, description=self.name + " talks to " + target.name)

    def hug(self, target):
        return Intention(self, "hug", target, description=self.name + " hugs " + target.name)

    def give(self, target):
        return Intention(self, "give", target, description=self.name + " gives a gift to " + target.name)

    def praise(self, target):
        return Intention(self, "praise", target, description=self.name + " praises " + target.name)

    def rebuke(self, target):
        return Intention(self, "rebuke", target, description=self.name + " rebukes " + target.name)

    def dance(self):
        return Intention(self, "dance", description=self.name + " dances")

    def die(self):
        return Intention(self, "die", description=self.name + " dies")

    def updateExperience(self, experiences):
        # Update this NPC's experiences
        pass

    def step(self, location):
        # What to do?
        if self.health == 0:
            return self.die()

        # Heal over time, get hungry over time, 
        self.health += 1 if self.health < 100 and self.hunger < 100 else 0
        self.hunger += 1 if self.hunger < 0 else 0
        self.health -= 1 if self.hunger == 100 else 0

        # Do we have anyone we love
        candidates = [(c, self.friends[c]) for c in self.friends if self.friends[c] > 50]
        if len(candidates) > 0:
            candidates = sorted(candidates, key=lambda candidate: candidate[1], reverse=True)
            self.love = candidates[0]

        # Check and Set Goals Applying Emotional Reasoning.
        options=location.availableActions(self)
        needs = self.getMaslowHierarchy()
        
        #TODO: How are we mapping needs to possible actions - won't this rely on experience?
        # Setting goals, setting motivations

        # Do things?
        if self.sleeping > 0:
            return self.zzz()
        if self.stamina <= 0:
            return self.sleep()

        # Do Random thing.
        shrug = random.choice(options)
        if shrug == "travel":
            direction = random.choice(["North", "South", "East", "West"])
            return self.travel(direction)
        elif shrug in ["attack", "talk", "hug", "give", "praise", "rebuke"]:
            target = random.choice([x for x in location.actors if x != self])
            return self.actions[shrug](target)
        else:
            return self.actions[shrug]()

        

        
class Monster(NPC):
    """Monster"""
    def __init__(self, name="Monster", health=20, strength=10, food=4, **kwargs):
        NPC.__init__(self, name, health=health, strength=strength, food=food, **kwargs)
        self.health = health # If we want to have varying difficulty monsters
        self.shitList = deque(maxlen=5)
        self.aggression = 0.25
    
    def step(self, location):
        # If someone interacted with it, and they're still around. Attack them.
        self.shitList = deque(sorted(self.shitList, key=lambda e: e[1]))
        while len(self.shitList) > 0:
            target = self.shitList.pop()
            if target in location:
                break
        else:
            target = None

        if target:
            return Intention(self, "attack", target, self.name + " attacks " + choice.name)

        # Do I want to attack?
        if len(location.actors) > 1 and random.random() < self.aggression:
            # Yes, Yes I do. Look... fresh meat.
            choice = None
            while not choice or choice == self:
                choice = random.choice(location.actors)
            return Intention(self, "attack", choice, self.name + " attacks " + choice.name)
        else:
            # Sleep
            return Intention(self, "zzz", None, self.name + " snoozes")

    def updateExperiences(self, experiences):
        for intent, experience in experiences:
            if intent.target == self:
                # You made my list.
                if intent.action == "attack":
                    #You attacked me!?
                    self.shitList.append((e[0], 2))
                else:
                    # You dare disturb me!?
                    self.shitList.append((e[0], 1))