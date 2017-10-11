#Base Action Class
class Base:
    def __init__(self, name, desc, **kwargs):
        print("KWARGS="+str(kwargs))
        self.name = name
        self.desc = desc
        self.locations = kwargs.get("locations", []) # A list of locations this action is specifically relevant to.
        self.sourceItemDelta = kwargs.get("sourceItemDelta", {})
        self.targetItemDelta = kwargs.get("targetItemDelta", {})
        self.sourceNeedsDelta = kwargs.get("sourceNeedsDelta", {})
        self.targetNeedsDelta = kwargs.get("targetNeedsDelta", {})
        self.sourceFeelingsDelta = kwargs.get("sourceFeelingsDelta", {})
        self.targetFeelingsDelta = kwargs.get("targetFeelingsDelta", {})
        self.locationChange = kwargs.get("locationChange", 0)

    def perform(self, source, target, location):
        # Update Inventories
        if self.locationChange:
            if location.directions[target].isAccessible():
                location.directions[target].actors.append(source)
                location.actors.remove(source)
            else:
                return "{0} cannot be performed by {1} towards {2}".format(self.name,source.name,target)
                
        targetStr = source.name if target==None else (target if isinstance(target, str) else target.name)
        if len(self.sourceItemDelta) > 0 and not source.updateInventory(self.sourceItemDelta, target, location): return "{0} cannot be performed by {1} on {2}".format(self.name,source.name,targetStr)
        if len(self.targetItemDelta) > 0 and not target.updateInventory(self.targetItemDelta, target, location): return "{0} cannot be performed by {1} on {2}".format(self.name,source.name,targetStr)
        if len(self.sourceNeedsDelta) > 0: source.updateNeeds(self.sourceNeedsDelta, target, location)
        if len(self.targetNeedsDelta) > 0: target.updateNeeds(self.targetNeedsDelta, source, location)
        if len(self.sourceFeelingsDelta) > 0: source.updateFeelings(self.sourceFeelingsDelta, target, location)
        if len(self.targetFeelingsDelta) > 0: target.updateFeelings(self.targetFeelingsDelta, source, location)

        return self.desc.format(source.name, target, location.name)
        


# The Basic Action subclasses
class Action(Base):
    pass

class Interaction(Base):
    pass

class Movement(Base):
    pass