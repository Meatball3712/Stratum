# Gloom Stalker - Monster
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from races.base import Monster

class GloomStalker(Monster):
    """Eadrite Class"""
    def __init__(self, name, SA, AA, **kwargs):
        super().__init__(name, SA, AA, **kwargs)