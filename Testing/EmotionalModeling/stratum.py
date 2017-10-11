#!python3
from world import WorldMap
import races
from ai import *

import logging, argparse
from logging.handlers import RotatingFileHandler
import time

def setupDefaultLogging(verbose=False):
    # Setup Default Logging
    logger = logging.getLogger("SimpleWorld")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    h = logging.StreamHandler()
    h.setLevel(logging.DEBUG)
    h.setFormatter(fmt)
    logger.addHandler(h)

    fmt = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    h = RotatingFileHandler("EMTesting.log", maxBytes=1000000, backupCount=5)
    h.setLevel(logging.INFO)
    h.setFormatter(fmt)
    logger.addHandler(h)

    return logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STRATUM - Interactive AI Test")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True, default=False, help= "Print debug logging to screen")
    parser.add_argument('-l', '--learn', dest='learn', action='store_const', const=True, default=False, help= "Enable Learning Mode, or just run")
    kwargs = vars(parser.parse_args())
    logger = setupDefaultLogging(verbose=kwargs["verbose"])

    # Create World
    STRATUM = WorldMap(logger=logger)
    
    # Create Characters and Initialise AI - XXX needs to be replaced by actual implementation
    Eadrite = races.getRace("Eadrite")
    GloomStalker = races.getRace("Gloom Stalker")
    for name in ("Ilex","Holly","Azolla","Calamis"):
        c = Eadrite(name=name, SA=SituationalAnalysis.SituationAnalyser(), AA=ActionAnalysis.ActionAnalyser(), logger=logger)
        STRATUM["Warden Town"].addCharacter(c)

    # Add Monster in the Forest
    m = GloomStalker(name="The Dread Seeker", SA=SituationalAnalysis.SituationAnalyser(), AA=ActionAnalysis.ActionAnalyser(), logger=logger)
    STRATUM["Gloomwood Forest"].addCharacter(m)
        

    try:
        while True:
            # Main Loop
            for location in STRATUM:
                for c in location.characters:
                    c.anticipate(location)

            for location in STRATUM:
                for c in location.characters:
                    c.react(location)

            # Print world State

    except KeyboardInterrupt:
        # Shutdown
        logger.info("Shutting Down")
        # Print Final World State.
        
