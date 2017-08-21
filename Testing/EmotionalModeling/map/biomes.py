# All the world Biomes

class Biome():
    """Base Biome Class"""
    def __init__(self, name, **kwargs):
        # Name
        self.name = name
        self.description = kwargs.get("description", "")

        # Directions
        self.north = kwargs.get("north", None)
        self.south = kwargs.get("south", None)
        self.east = kwargs.get("east", None)
        self.west = kwargs.get("west", None)

        # Inhabitants
        self.inhabitants = []


class Farm(Biome):
    """Farm Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
class Plain(Biome):
    """Plain Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

class Forest(Biome):
    """Forest Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
class Village(Biome):
    """Village Biome"""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)