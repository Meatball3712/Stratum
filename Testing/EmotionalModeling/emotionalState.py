# PAD Model

class EmotionalState:
    def __init__(self, currentState=(0,0,0)):
        self.mood = currentState # Default to neutral

class PADMap:
    def __init__(self):
        # Model P,A,D values to moods
        self.extents = {
        "Exuberant" : (1.,1.,1.),
        "Dependant" : (1.,1.,-1),
        "Relaxed"   : (1.,-1.,1.),
        "Docile"    : (1.,-1.,-1.),
        "Bored"     : (-1.,-1.,-1.),
        "Disdainful": (-1.,-1.,1.),
        "Anxious"   : (-1.,1.,-1.),
        "Hostile"   : (-1.,1.,1.)
        }

        self.emotions = 

class OCCMap:
    def __init__(self):
        metrics = (
            "desirability"
            "actions"
            "consequences"
            "expectations"
            "affects",
            "familiarity",
            "favour"
        )

        feelings = 

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
approving is being positive about an action (of an agent)
disapproving is being negative about an action (of an agent)
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