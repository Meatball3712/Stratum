# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.



class Monster:
    """Monster"""
    def __init__(self, health):
        self.name = "Monster"
        self.health = health # If we want to have varying difficulty monsters
        self.food = 75
        self.attack = 10
    
    def step(self, location):
        return []

class NPC:
    def __init__(self, name):
        self.name = name

         # Set goals based on Heirarchy of needs?
        # Physiology - Food/Water/Breathing etc. (May not be relevent unless we want to make a survival game)
        self.hunger = 0
        self.stamina = 100
        self.sleeping = 0
        self.strength = 20 # How hard we attack
        self.food = 0
        
        # Safety - Security of body, family, health, resources
        self.health = 100

        # Love/Belonging - Friendship/Family/Intimacy
        self.belonging = 0 # How many people call me friend. Do I love anyone
        self.friends = {}
        self.love = None
        self.rivals = {}
        # Talking with someone increases friendliness, as does recieving praise
        # unless that person is a rival love interest (relative friendliness to our prospective mate)


        # Esteem - Confidence, Achievement, respect of and by others.
        # Earned by offering and recieving praise, deminished by rebukes
        self.respectedBy = 0
        self.respectForOthers = 0

        # Self-Actualisation: Morality, Creativity, Spontaneity, problem solving, lack of prejudice acceptance of facts (How to model this!?)
        self.dances = 0 # How many dances have we had. We can only dance when all other criteria are satisfied. A measure of fulfillment

        self.actions = {
            "sleep" : self.sleep,
            "attack" : self.attack,
            "run" : self.run,
            "travel" : self.travel,
            "talk" : self.talk,
            "hug" : self.hug,
            "praise" : self.praise,
            "rebuke" : self.rebuke,
            "give" : self.give,
            "dance" : self.dance
        }
    
    def travel(self, location):
        #TODO: change this whole thing to use the travel attached to the location
        pass

    def attack(self, target):
        # Decrease Hunger if monster.
        self.stamina -= 20
        if target == isinstance(Monster):
            self.health -= target.attack
            
            target.health -= self.strength

            if target.health <= 0:
                self.food += target.food

        else:
            target.health -= self.strength

        return self.name + " attacks " + target.name

    def eat(self):
        if self.food > 0:
            self.food -= 1
            self.hunger -= 25
            if self.hunger < 0: self.hunger = 0
            return self.name + " eats some food"

    def run(self):
        # You flee takes stamina, but you avoid taking damage
        self.stamina -= 20
        return self.name + " runs away"

    def zzz(self):
        if self.sleeping > 0: self.sleeping -= 1
        return self.name + " sleeps"

    def sleep(self):
        # Sleep for 5 turns or something
        self.sleeping = 5
        self.stamina = 100
        return self.name + " goes to sleep"

    def talk(self, target):
        # increase friendship rating with one npc.
        if target not in self.rivals and target.sleeping == 0:
            if target not in self.friends:
                self.friends[target] = 0
            self.friends[target] += 5 # Minor Social improvement
            return self.name + " talks to " + target.name

    def hug(self, target):
        # You can only hug someone who considers you their love. No cheating.
        if target.love == self and target.sleeping == 0:
            target.friends[self] += 20 # Big boost to friendliness - reinforces you as their lover.
            return self.name + " hugs " + target.name

    def recieve(self, source):
        # Receive a gift of food. Probably modified by hunger/how much food we have
        self.food += 1
        if source in self.rivals: # giving me a sandwich doesn't mean we're friends
            return False

        elif source not in self.friends:
            self.friends[source] = 0

        self.friends[source] += 10 # a gift of food is better than a chat
        return self.name + " receives a gift from " + target.name


    def give(self, target):
        # Maybe in the future.
        if self.food > 0 and target.sleeping == 0:
            target.recieve(self)
            self.food -= 1
            return self.name + " gives a gift to " + target.name

    def praise(self, target):
        if target.sleeping == 0:
            if target not in self.respectForOthers:
                self.respectForOthers[target] = 0
            self.respectForOthers[target] += 5
            target.getPraised(self)
            return self.name + " praises " + target.name

    def getPraised(self, source):
        if source not in self.respectedBy:
            self.respectedBy[source] = 0
        self.respectedBy[source] += 5
        return self.name + " receives praise from " + target.name

    def rebuke(self, target):
        if target.sleeping == 0:
            if target in self.respectForOthers and self.respectForOthers[target] > 0:
                self.respectForOthers[target] -= 5
            target.getRebuked(self)
            return self.name + " rebukes " + target.name

    def getRebuked(self, source):
        if source in self.respectedBy and self.respectedBy[source] > 0:
            self.respectedBy[source] -= 5
        return self.name + " is rebuked by " + target.name

    def dance(self):
        # You can only dance when other needs are met.
        self.stamina -= 50
        if self.hunger < 25 and self.health == 100 and self.stamina > 50 and self.food > 0 and self.love != None and self.love.target == self:
            dance += 1
            return self.name + " dances"

    def step(self, location):
        # What to do?
        # Heal overtime, get hungry overtime, 
        self.health += 1 if self.health < 100 and self.hunger < 100 else 0
        self.hunger += 1 if self.hunger < 0 else 0
        self.health -= 1 if self.hunger == 100 else 0

        # Do we have anyone we love
        candidates = [(c, self.friends[c]) for c in self.friends if self.friends[c] > 50]
        if len(candidates) > 0:
            candidates = sorted(candidates, key=lambda candidate: candidate[1], reverse=True)
            self.love = candidates[0]


        # Do things?
        action = []
        if self.sleeping > 0:
            action = [self.zzz,self]
        if self.stamina <= 0:
            action = [self.sleep, self]
        #if action is still empty, do other stuff
        return action
        
