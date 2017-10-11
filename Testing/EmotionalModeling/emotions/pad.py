#!python3
# PAD Model
import sys, os
sys.path.insert(0, os.path.abspath('..'))import numpy as np

import csv, json

# PAD Model
class PADMap:
    def __init__(self):
        # Model P,A,D values to moods
        self.emotions = {}
        # Load EmotionalModel
        with open("PADMappings.csv", "r") as f:
            reader = csv.reader(f)
            headers = next(reader,None)
            for e,p,a,d in reader:
                self.emotions[e] = np.array((float(p), float(a), float(d)))

    def __contains__(self, emotion):
        if emotion in self.emotions:
            return True
        return False

    def __getitem__(self, emotion):
        if emotion in self.emotions:
            return self.emotions[emotion]
        raise KeyError("Unknown Emotion ({}) specified.".format(emotion))

    def getValence(self, emotion):
        if emotion in self.emotions:
            return self.emotions[emotion][0]
        raise KeyError("Unknown Emotion ({}) specified.".format(emotion))

    def getArousal(self, emotion):
        if emotion in self.emotions:
            return self.emotions[emotion][1]
        raise KeyError("Unknown Emotion ({}) specified.".format(emotion))

    def getDominance(self, emotion):
        if emotion in self.emotions:
            return self.emotions[emotion][2]
        raise KeyError("Unknown Emotion ({}) specified.".format(emotion))