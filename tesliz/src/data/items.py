from tactics.Affect import *

#vaule should be the quivalent to the lowest level that the units should be outfitted
#with this item
class Item():
    def setup(self,unit):
        if hasattr(self, "affects"):
            self.affects.setup(unit)
    def getName(self):
        return self.__class__.__name__
    value = 1
    type = "none"
    allowed = []
class Potion(Item):
    affects = Affects(StatAffect(["physical","points"],30),"       hitpoints") 
    
    mesh = "plane.mesh"

class ClothCap(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],5),"       hitpoints") 

    mesh = "cylinder.mesh"
    type= "head"
    value = 1
    
class Helm(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],10),"       hitpoints") 
    allowed = ["Knight"]
    
    type= "head"
    value = 2
class LeatherArmor(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],10),"       hitpoints") 
    allowed = ["Squire","Knight","Poet"]
    mesh = "cylinder.mesh"
    type = "body"
    value = 1
class PlateArmor(Item):
    affects = Affects(StatAffect(["physical","maxpoints"],20),"       hitpoints") 
    allowed = ["Knight"]
    
    type = "body"
    value = 2
class Broadsword(Item):
    power = 4
    type = "weapon"
    value = 1
class Knightsword(Item):
    power = 5
    type = "weapon"
    value = 2
    
class Dagger(Item):
    power = 2
    type = "weapon"
    value = 1