from story import Story
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

#Make sure Class is UPPER case of module name
class TRIANGLES(Story):
    """
    The story of Riley, Obin and Hali

    Trangles of interest

    Setup
    Riley and Obin are friends
    Riley has developed a fondness for Hali,
    but Hali has eyes only for Obin

    Standard Love Triangle trope.
    Jealousy, Love, Regret, Tradgedy

    How would this play out in our emotional engine?

    """

    def __init__(self):
        Story.__init__(self)

        # Props
        Fruit = self.addProp("Fruit")

        # Characters
        Riley = self.addCharacter(
            "Riley", 
            "A young eager boy. Excitable but with a secret crush on Hali", 
            (0.75,0.2,0.75)
        )

        Hali = self.addCharacter(
            "Hali", 
            "A sweet, shy, girl. She has a crush on Obin",
            (0.6,0.2,0)
        )

        Obin = self.addCharacter(
            "Obin",
            "The eldest of the three, he is more mature and is generally admired by his peers, but can be a little clueless sometimes.",
            (0.5,0.2,0.75)
        )

        # Character World Views.
        # Riley
        Riley.addWorldView("Object", "Fruit",0.5) # Riley really likes fruit 
        Riley.addWorldView("Character", "Hali", 0.9) # Riley really likes Hali
        Riley.addWorldView("Character", "Obin", 0.8) # Riley is good friends with Obin
        Riley.addWorldView("Experience", "Tasty", 0.8) # Riley likes tasty things
        Riley.addNeed("food")
        Riley.addWant("food")
        Riley.addNeed("love")
        Riley.addWant("affection")
        Riley.addGoal("converse", Hali)
        
        # 
        Hali.addWorldView("Object", "Fruit", 0.5) # Hali likes Fruit
        Obin.addWorldView("Object", "Fruit", 0.5) # Obin likes Fruit


        ######  Chapter 1  #####
        description = """
        Riley saunters down the village road, a spring in his step and a song on his lips. It's a beautiful day, 
        and it's a perfect opportunity to visit the girl of his dreams. On his way, he spots his good friend Obin
        who is coming from his families farm carrying some freshly picked fruit. 

        Riley greets Obin with a hearty wave.
          "Hey Obin, how are you?"
        """

        # Events = affects, agent, target, action, probability, consequence, description=""
        events = [
            (
                Riley, # Who's perspective is this?
                Riley, # Initiator
                Obin, # Target
                "greet", #Action
                1, # Expectation 0 = impossible, 1 = certain
                "greet" # Expected Consequence
            ),
            (
                Obin,
                Riley,
                Obin,
                "greet"
            ),
        ]

        self.addChapter(description, events)

        ##### Chapter 2 #####
        description = """
        Obin, hearing his name called, looks up. He smiles when he see's his plucky friend jogging towards him.
          "Hi Riley, nice day isn't it. Just got the first picks of the summer harvest. Should be a good one this year."

        Riley eyes the delicious looking fruit with a gurgle in his stomach. He skipped breakfast that morning. 
        But he didn't want to ask for any of the fruit, he didn't want to impose on the older farm boy. That was rude.
        """

        events = [
            (
                Obin,
                Obin,
                Riley,
                "greet",
                1,
                "converse"
            ),(
                Riley,
                Obin,
                Riley,
                "offer",
                0.5,
                "gift"
            ),(
                Riley,
                Riley,
                Fruit,
                "eat",
                0.9,
                "tasty"
            ),
        ]

        self.addChapter(description, events)