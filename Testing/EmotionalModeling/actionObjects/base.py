#Base Action Class
class Action():
    """Base Action Class"""
    def __init__(self, name, desc, **kwargs):
        self.name = name
        self.desc = desc
        self.locations = [] # A list of locations this action is specifically relevant to.
        self.sourceItemDelta = kwargs.get("sourceItemDelta", {})
        self.targetItemDelta = kwargs.get("targetItemDelta", {})
        self.sourceNeedsDelta = kwargs.get("sourceNeedsDelta", {})
        self.targetNeedsDelta = kwargs.get("targetNeedsDelta", {})
        self.sourceFeelingsDelta = kwargs.get("sourceFeelingsDelta", {})
        self.targetFeelingsDelta = kwargs.get("targetFeelingsDelta", {})
        self.locationChange = kwargs.get("locationChange", 0)

    def __str__(self, source, target, location):
        return self.desc.format(source, target, location)

    def perform(self, source, target, location):
        # do standard stat updates here.
        #for key, value in self.source
            #if key in source.stats
            #  source.stats[key] += value
            # etc...
        pass
