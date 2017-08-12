# PAD Model
class PADMap:
    def __init__(self):
        # Model P,A,D values to moods
        self.extents = {
        "exuberant" : (1.,1.,1.),
        "dependant" : (1.,1.,-1),
        "relaxed"   : (1.,-1.,1.),
        "docile"    : (1.,-1.,-1.),
        "bored"     : (-1.,-1.,-1.),
        "disdainful": (-1.,-1.,1.),
        "anxious"   : (-1.,1.,-1.),
        "hostile"   : (-1.,1.,1.)
        }

class OCCMap:
    """ Mapping the Ortony, Clore and Collins Model to the PAD Model """
    def __init__(self):
        """Map Experiences according to 
        desirability
        actions
        consequences
        expectations
        affects
        familiarity
        favour
        """
        feelings = None

        self.mappings = [
            "hope",
            "fear",
            "joy",
            "distress",
            "satisfaction",
            "dissapointment",
            "relief",
            "fears-confirmed",
            "happy-for",
            "resentment",
            "gloating",
            "pity",
            "approving",
            "disapproving",
            "pride",
            "shame",
            "admiration",
            "reproach",
            "gratification",
            "remorse",
            "gratitude"
        ]

    def map(self):
        """ Map OCC to PAD """
        

# Map of Action keywords to their related extent (this will vary to degrees of course)
actionLibrary = {
    # Exchange
    "offer" : "relaxed"
    "impose" : "disdainful",
    "steal" : "hostile",
    "gift" : "dependant",
    "compliment" : "docile",
    "attack" : "hostile",
    "defend" : "hostile",
    "eat" : "exuberant"
}

class Personality:
    def __init__(self, currentState=(0,0,0)):
        self.mood = currentState # Default to neutral
        self.worldView = {} # Dictionary of Valency's on all sorts of topics, people and things.

        # Action Planning - not exactly emotions, but emotions are influenced by the following.
        self.needs = {} # What does this personally actually need regardless of what they think they need
        self.goals = {} # List of personal goals based on desires, which may or maynot satisfy needs.
        self.plans = [] # List of plans aimed to satisfy goals.

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
        # Talking with someone increases friendliness, unless that person is a rival love interest (relative friendliness to our prospective mate)


        # Esteem - Confidence, Achievement, respect of and by others.

        # Self-Actualisation: Morality, Creativity, Spontaneity, problem solving, lack of prejudice acceptance of facts (How to model this!?)


    def addNeed(self, need, valence):
        self.needs[need] = valence

    def addGoal(self, desire, valence):
        self.goals[desire] = valence

    def how_do_I_feel_about(self, initiator=None, target=None, action=None, consequence=None):
        """ How do I feel about things. People, Actions, Consequences """
        # Return -1 <= x <= 1
        return 1

    def what_I_think_is_going_to_happen(self, action, initiator, target):

        return None

    def experience(self, **kwargs):
        # initiator - a valence on how we feel about the causer
        # target - a valence on how we feel about the target
        # action - a valence on the action maybe - otherwise it is irrelevant except to predict consequence.
        # expectation - how likely we believe the consequence will occur. None if it's happening.
        # consequence - our percieved valence on an outcome.
        initiator = kwargs["initiator"], 
        target = kwargs["target"]
        action = kwargs["action"]
        expectation = kwargs.get("expectation", None)
        consequence = kwargs.get("consequence", None)
        
        feelings = {}
        hif_ConsequenceObjectively = self.how_do_I_feel_about(consequence) # Without context, is this a positive consequence
        hif_ConsequenceSubjectively = self.how_do_I_feel_about(consequence, initiator, target) # Within context, do I now feel positive about it?
        hif_initiator = self.how_do_I_feel_about(initiator) # Personal opinion of the initator
        hif_target = self.how_do_I_feel_about(target) # Personal opinion of the target
        hif_actionObjectively = self.how_do_I_feel_about(action) # Opinion of an action without a context
        hif_actionSubjectively = self.how_do_I_feel_about(action, initiator, target) # Opinion of the action in this context
        AnticipatedConsequence = self.what_I_think_is_going_to_happen(action, initiator, target) # What do we expect to happen?
        hif_AnticipatedConsequence = self.how_do_I_feel_about(AnticipatedConsequence)

        # Is this outcome important to us?
        if hif_ConsequenceSubjectively != 0:

            if expectation != None
                if hif_ConsequenceSubjectively > 0:
                    # Chance of Good Outcome
                    feelings["hope"] = abs(hif_ConsequenceSubjectively*expectation)
                elif expectation != None and hif_ConsequenceSubjectively < 0:
                    # Chance of Bad Outcome
                    feelings["fear"] = abs(hif_ConsequenceSubjectively)

            else:
                if hif_ConsequenceSubjectively > 0:
                    # Good Outcome
                    feelings["joy"] = abs(hif_ConsequenceSubjectively)
                else:
                    # Bad Outcome
                    feelings["distress"] = abs(hif_ConsequenceSubjectively)


                # Expectations
                if AnticipatedConsequence:
                    # We had expectations on this outcome, compounding our feelings.
                    if hif_AnticipatedConsequence > 0 and hif_ConsequenceSubjectively > 0:
                        # Confirmation of Expected Good Outcome
                        feelings["satisfaction"] = abs(hif_ConsequenceSubjectively)
                    elif hif_AnticipatedConsequence > 0 and hif_ConsequenceSubjectively < 0:
                        # Rejection of Expected Good Outcome
                        feelings["dissapointment"] = abs(hif_ConsequenceSubjectively)
                    elif hif_AnticipatedConsequence < 0 and hif_ConsequenceSubjectively > 0:
                        # Rejection of Expected Bad Outcome
                        feelings["relief"] = abs(hif_AnticipatedConsequence)
                    else:
                        # Confirmation of Expected Bad Outcome
                        feelings["fears-confirmed"] = abs(hif_AnticipatedConsequence)

                # Empathy
                if target != self:
                    if feelings.has_key("joy") and hif_ConsequenceObjectively > 0:
                        feelings["happy-for"] = abs(hif_ConsequenceSubjectively)
                    elif feelings.has_key("distress") and hif_ConsequenceObjectively > 0:
                        feelings["resentment"] = abs(hif_ConsequenceSubjectively)
                    elif feelings.has_key("joy") and hif_ConsequenceObjectively < 0:
                        feelings["gloating"] = abs(hif_ConsequenceSubjectively)
                    else:
                        feelings["pity"] = abs(hif_ConsequenceSubjectively)

                # Evaluation of Action
                if hif_actionObjectively > 0: feelings["approving"] = abs(hif_actionObjectively)
                elif hif_actionObjectively < 0: feelings["disapproving"] = abs(hif_actionObjectively)

                # Ego
                if self == initiator and hif_actionObjectively != 0:
                    if hif_actionObjectively > 0:
                        feelings["pride"] = abs(hif_actionObjectively)
                    elif hif_actionObjectively < 0:
                        feelings["shame"] = abs(hif_actionObjectively)

                # Judgement
                elif hif_actionObjectively != 0:
                    if hif_actionObjectively > 0:
                        feelings["admiration"] = abs(hif_actionObjectively)
                    elif hif_actionObjectively < 0:
                        feelings["reproach"] = abs(hif_actionObjectively)

                # Resolution
                if feelings.has_key("pride") and feelings.has_key("joy"):
                    feelings["gratification"] = (feelings["pride"]+feelings["joy"]) / 2.0
                elif feelings.has_key("shame") and feelings.has_key("distress"):
                    feelings["remorse"] = (feelings["shame"]+feelings["distress"]) / 2.0
                elif feelings.has_key("admiration") and feelings.has_key("joy"):
                    feelings["gratitude"] = (feelings["admiration"]+feelings["joy"]) / 2.0
                elif feelings.has_key("reproach") and feelings.has_key("distress"):
                    feelings.has_key("anger") = (feelings["reproach"]+feelings["distress"]) / 2.0

                # Catalog Experience for future context
                return feelings



"""
positive and negative are valenced reactions (to “something”)
pleased is being positive about a consequence (of an event)
displeased is being negative about a consequence (of an event)
hope is being pleased about a prospective consequence (of an event)
fear is being displeased about a prospective consequence (of an event)
joy is being pleased about an actual consequence (of an event)
distress is being displeased about an actual consequence (of an event)

satisfaction is joy about the confirmation of a prospective desirable consequence
fears-confirmed is distress about the confirmation of a prospective undesirable consequence
relief is joy about the disconfirmation of a prospective undesirable consequence
disappointment is distress about the disconfirmation of a prospective desirable consequence


happy-for is joy about a consequence (of an event) presumed to be desirable for someone else
resentment is distress about a consequence (of an event) presumed to be desirable for someone else
gloating is joy about a consequence (of an event) presumed to be undesirable for someone else
pity is distress about a consequence (of an event) presumed to be undesirable for someone else

approving is being positive about an action (of an initiator)
disapproving is being negative about an action (of an initiator)
pride is approving of one’s own action
shame is disapproving of one’s own action
admiration is approving of someone else’s action
reproach is disapproving of someone else’s action
gratification is pride about an action and joy about a related consequence
remorse is shame about an action and distress about a related consequence
gratitude is admiration about an action and joy about a related consequence
anger is reproach about an action and distress about a related consequence
liking is being positive about an aspect (of an object)
disliking is being negative about an aspect (of an object)
love is liking a familiar aspect (of an object)
hate is disliking a familiar aspect (of an object)
interest is liking an unfamiliar aspect (of an object)
disgust is disliking an unfamiliar aspect (of an object)

"""


if __name__=="__main__":
    # Run Testing
    pass