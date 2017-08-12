# Emotive Agent
# Testing the machine learning capabilities for emotional intelligence.

class NPC:
	def __init__(self, name):
		self.name = name

		 # Set goals based on Heirarchy of needs?
        # Physiology - Food/Water/Breathing etc. (May not be relevent unless we want to make a survival game)
        self.hunger = 0
        self.stamina = 100
        
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

    
