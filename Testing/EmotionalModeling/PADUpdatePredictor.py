import numpy as np
import pickle

class Situation:
    
    location = None
    actors = None
    
    def __init__(self, character, actors, location):
        """
        Build the vector representations needed by the predictor
        """
        self.location = location.getVector()
        self.actors = ([np.hstack(
                            [a.getVector(a is character), 
                            character.getOpinionVector(a)]) 
                        for a in actions])

class PADUpdatePredictor:
    """
    PADUpdatePredictor learns an association of situation -> PAD outcome
    based on past experiences.
    """
    model = None
    
    def __init__(self, modelFileName = None):
        if modelFileName is not None:
            if isinstance(model, str):
                self.model = pickle.load(open(modelFileName,'r'))
            else:
                self.model = modelFileName
    
    def Observe(self, situation, PADDelta):
        if model is not None:
            model.update(situation, PADDelta)
    
    def Predict(self, situation):
        if model is not None:
            return model.predict(situation)
        return np.array((0.,0.,0.))
        
