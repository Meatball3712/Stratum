#story.py
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import EmotionalState

class Story:
    def __init__(self):
        self.agents = {} # The players on the field. They that can experience emotion.
        self.subjects = {} # Subjects of affection or disgust. From Brocolli to gold to holidays and weddings
        self.chapterCount = 0
        self.chapter = [] # A list of chapters

    def next(self):
        """ Read the next chapter of the story, and resolve the emotional states of the players """
        if self.chapterCount >= len(self.chapter):
            raise StopIteration("Fin")

        for event in self.chapter(chapterCount):
            # Resolve the events
            print(event.description)
            print(event.vector)

        self.chapterCount += 1

