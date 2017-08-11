#story.py
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import EmotionalState

class Chapter:
    def __init__(self, description):
        self.description = description
        self.events = []

    def addEvent(self, affects, agent, target, action, probability=None, consequence=None, description=""):
        self.events.append(Event(affects, agent, target, action, probability, consequence, description))

class Event:
    def __init__(self, affects, agent, target, action, probability=None, consequence=None, description=""):
        self.description = description
        self.affects = affects # The characters's who are experiencing the event. Who this affects.
        self.agent = agent
        self.target = target
        self.action = action
        self.probability = probability
        self.consequence = consequence

class Prop:
    def __init__(self, name):
        self.name = name
        self.type = "Obj"

class Story:
    def __init__(self, **kwargs):
        self.characters = {} # The players on the field. They that can experience emotion.
        self.props = {} # Subjects of affection or disgust. From Brocolli to gold to holidays and weddings
        self.chapterCount = 0
        self.chapters = [] # A list of chapters
        self.debug = kwargs.get("debug", True)

    def addCharacter(self, name, bio="", currentState=(0,0,0)):
        """ Add an actor to the stage """
        if self.debug:
            print("Introducing {name}".format(name=name))
            print(bio)
        character = EmotionalState.Personality(name, bio, currentState)
        self.characters[name] = character
        return character

    def addProp(self, name)
        """ Items that have no personality, but might be liked or unliked by the characters """
        prop = Prop(name)
        self.props[name] = prop
        return prop

    def addChapter(self, description, events):
        """ Add a chapter """
        chapter = Chapter(description)
        for event in events:
            chapter.addEvent(*event)
        self.chapters.append(chapter)

    def __iter__(self):
        self.chapterCount = 0
        return self

    def __next__(self):
        """ Read the next chapter of the story, and resolve the emotional states of the players """
        if self.chapterCount >= len(self.chapters):
            raise StopIteration("Fin")

        self.chapterCount += 1

        return self.chapters[chapterCount]