from tactics.Affect import *


class Item():
    def setup(self,unit):
        if hasattr(self, "affects"):
            self.affects.setup(unit)
    def getName(self):
        return self.__class__.__name__
    value = 1
    type = "none"
class Potion(Item):
    affects = Affects(StatAffect(["physical","points"],30),"       hitpoints") 
    allowed = ["all"]
    mesh = "plane.mesh"

class ClothCap(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],5),"       hitpoints") 
    allowed = ["all"]
    mesh = "cylinder.mesh"
    type= "head"
    value = 2
class LeatherArmor(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],10),"       hitpoints") 
    allowed = ["Squire","Knight"]
    mesh = "cylinder.mesh"
    type = "body"
    value = 2
class Broadsword(Item):
    power = 4
    type = "weapon"
    value = 2
    
class Dagger(Item):
    power = 2
    type = "weapon"
    value = 1