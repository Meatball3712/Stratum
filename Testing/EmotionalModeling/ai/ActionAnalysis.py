#!python3
import sys, os
sys.path.insert(0, os.path.abspath('..'))

import numpy as np
import pickle

class ActionEvent:
    
    actors = None
    event = None
    
    def __init__(self, character, action, target, actors, location):
        """
        Build the vector representations needed by the predictor
        """
        self.actors = ([np.hstack(
                            [a.getVector(a is character), 
                            character.getOpinionVector(a)]) 
                        for a in actions])
        cv = character.getVector(True)
        av = action.getVector()
        tv = None
        if target is None:
            tv = np.hstack(cv*0., character.getOpinionVector(character)*0.])
        else:
            tv = np.hstack(target.getVector(), character.getOpinionVector(target)])
        self.event = np.hstack(cv, av, tv, location.getVector())

class ActionAnalyser:
    """
    ActionAnalyser learns an association of:
    action + situation => long term reward
    based on past experiences.
    """
    model = None
    
    def __init__(self, modelFileName = None):
        if modelFileName is not None:
            if isinstance(model, str):
                self.model = pickle.load(open(modelFileName,'r'))
            else:
                self.model = modelFileName
    
    def Observe(self, actionEvent, goalMeasure):
        if model is not None:
            model.update(situation, goalMeasure)
    
    def Predict(self, actionEvent):
        if model is not None:
            return model.predict(situation)
        return 0.
        
