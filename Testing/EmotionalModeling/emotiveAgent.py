# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.

class location:
    """Location Object"""
    def __init__(self, name, north=None, south=None, east=None, west=None):
        self.name = name
        self.directions = {}
        self.directions["north"] = north if north else self
        self.directions["south"] = south if south else self
        self.directions["east"] = east if east else self
        self.directions["west"] = west if west else self

    def travel(self, direction):
        if direction in self.directions:
            return self.directions[direction]
        else:
            return self

class Monster():
    """Monster"""
    def __init__(self, health):
        self.health = health # If we want to have varying difficulty monsters
        self.food = 75
        self.attack = 10

class NPC:
    def __init__(self, name, location):
        self.name = name
        self.location = location

         # Set goals based on Heirarchy of needs?
        # Physiology - Food/Water/Breathing etc. (May not be relevent unless we want to make a survival game)
        self.hunger = 0
        self.stamina = 100
        self.sleeping = 0
        self.strength = 20 # How hard we attack
        
        # Safety - Security of body, family, health, resources
        self.health = 100

        # Love/Belonging - Friendship/Family/Intimacy
        self.belonging = 0 # How many people call me friend. Do I call anyone a lover
        self.friends = []
        self.lover = None
        self.rivals = []
        # Talking with someone increases friendliness, as does recieving praise
        # unless that person is a rival love interest (relative friendliness to our prospective mate)


        # Esteem - Confidence, Achievement, respect of and by others.
        # Earned by offering and recieving praise, deminished by rebukes
        self.respectedBy = 0
        self.respectForOthers = 0

        # Self-Actualisation: Morality, Creativity, Spontaneity, problem solving, lack of prejudice acceptance of facts (How to model this!?)
        self.dances = 0 # How many dances have we had. We can only dance when all other criteria are satisfied.

        self.actions = {
            "sleep" : self.sleep,
            "attack" : self.attack,
            "run" : self.run,
            "travel" : self.travel,
            "talk" : self.talk,
            "hug" : self.hug,
            "praise" : self.praise,
            "rebuke" : self.rebuke,

        }


    def attack(self, target):
        # Decrease Hunger if monster.
        self.stamina -= 20
        if target == isinstance(Monster):
            self.health -= target.attack
            
            target.health -= self.strength

            if target.health <= 0:
                self.hunger -= target.food

        else:
            target.health -= self.strength

        if self.hunger < 0: self.hunger = 0
        if self.stamina <= 0: self.sleep()

    def run(self):
        # You flee takes stamina, but you avoid taking damage
        self.stamina -= 20


    def zzz(self):
        if self.sleeping > 0: self.sleeping -= 1

    def sleep(self):
        # Sleep for 5 turns or something
        self.sleeping = 5

    def travel(self, direction):
        # Pick a direction and move.
        self.location = self.location.travel(direction)


        