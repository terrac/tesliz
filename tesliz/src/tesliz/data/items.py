from tactics.Affect import *


class Item():
    def setup(self,unit):
        if hasattr(self, "affects"):
            self.affects.setup(unit)
class Potion(Item):
    affects = Affects(StatAffect(["physical","points"],30),"       hitpoints") 
    allowed = ["all"]
    mesh = "plane.mesh"

class ClothCap(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],5),"       hitpoints") 
    allowed = ["all"]
    mesh = "cylinder.mesh"
    type= "head"

class LeatherArmor(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],10),"       hitpoints") 
    allowed = ["all"]
    mesh = "cylinder.mesh"
    type = "body"
class Broadsword(Item):
    power = 4
    type = "weapon"
    
