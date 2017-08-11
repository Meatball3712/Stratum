#story.py
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from character import Character

class Chapter:
    def __init__(self, description):
        self.description = description
        self.events = []

    def addEvent(self, affects, initiator, target, action, probability=None, expectation=None, description=""):
        self.events.append(Event(affects, initiator, target, action, probability, expectation, description))

class Event:
    def __init__(self, affects, initiator, target, action, probability=None, expectation=None, description=""):
        self.description = description
        self.affects = affects # The characters's who are experiencing the event. Who this affects.
        self.initiator = initiator
        self.target = target
        self.action = action
        self.probability = probability
        self.expectation = expectation

    def args(self):
        return {
            "initiator": self.initiator
            "target" : self.target
            "action" : self.action
            "probability" : self.probability
            "expectation" : self.expectation
        }

class Prop:
    def __init__(self, name):
        self.name = name

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
        C = Character(name, bio, currentState)
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

    def read(self):
        """ Read a story, executing it's events etc """
        for chapter in self.chapters:
            print("\n\n{}\n".format(chapter.description))
            print("Events:\n")
            for event in chapter.events:
                if len(event.description)>0:
                    print("{}\n".format(event.description))
                else: 
                    print("Affecting {.affects}: {.initiator} \"{.action}\"(ed) {.target}".format(event), end="")
                    if event.probability:
                        print(" with expected {.probability:.2%} chance of {.expectation} \n".format(event.))
                    print()
                event.affects.experience(**event)
