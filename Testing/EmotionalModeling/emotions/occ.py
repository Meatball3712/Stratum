import numpy as np
import csv, json

class OCCMap:
    """ Mapping the Ortony, Clore and Collins Model to the PAD Model """
    def __init__(self):
        """ Map Experiences to reflected emotions """
        pass

    def how_do_I_feel_about(self, item):
        """ How do I feel about things. People, Actions, Consequences """
        # Return -1 <= x <= 1
        return None

    def what_I_think_is_going_to_happen(self, action, source, target):

        return None

    def experience(self, intent, location, experience):
        # exp = a dictionary of stat deltas

        # source - a valence on how we feel about the causer
        # target - a valence on how we feel about the target
        # action - a valence on the action maybe - otherwise it is irrelevant except to predict consequence.
        # expectation - how likely we believe the consequence will occur. None if it's happening.
        # consequence - our percieved valence on an outcome.
        source = kwargs["source"], 
        target = kwargs["target"]
        action = kwargs["action"]
        expectation = kwargs.get("expectation", None)
        consequence = kwargs.get("consequence", None)
        
        feelings = {}
        hif_ConsequenceObjectively = self.how_do_I_feel_about(consequence) # Without context, is this a positive consequence
        hif_ConsequenceSubjectively = self.how_do_I_feel_about(consequence, source, target) # Within context, do I now feel positive about it?
        hif_source = self.how_do_I_feel_about(source) # Personal opinion of the initator
        hif_target = self.how_do_I_feel_about(target) # Personal opinion of the target
        hif_actionObjectively = self.how_do_I_feel_about(action) # Opinion of an action without a context
        hif_actionSubjectively = self.how_do_I_feel_about(action, source, target) # Opinion of the action in this context
        AnticipatedConsequence = self.what_I_think_is_going_to_happen(action, source, target) # What do we expect to happen?
        hif_AnticipatedConsequence = self.how_do_I_feel_about(AnticipatedConsequence)

        # Is this outcome important to us?
        if hif_ConsequenceSubjectively != 0:

            if expectation != None:
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
                if self == source and hif_actionObjectively != 0:
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
                    feelings["anger"] = (feelings["reproach"]+feelings["distress"]) / 2.0

                # Catalog Experience for future context
                return feelings


# Text from OCC Model documentation - new and improved
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

approving is being positive about an action (of an source)
disapproving is being negative about an action (of an source)
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
        

# Map of Action keywords to their related extent (this will vary to degrees of course)
# Defaults
