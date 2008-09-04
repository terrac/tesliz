from tactics.util import *
import data.traits.Generictraits as GT
from userinterface.Numberedtraits import *
#from data.traits.GenericTraits import *
from tactics.Move import *
from tactics.Attack import *
#from data.traits.GenericTrait import Move
class Unittypes(object):
    def FastFighter(self,unit):
        unit.attributes.speed = 3
        unit.attributes.hitpoints = 50        
        unit.attributes.damage = 50
                       
    def SlowFighter(self,unit):
        unit.attributes.speed = 5
        unit.attributes.hitpoints = 50        
        unit.attributes.damage = 50
        
    def Mage(self,unit):
        unit.attributes.speed = 4
        
        #dir(GT)
        unit.traits["Move"] = NumberedTraits([Move()],[5])
        unit.traits["Attack"] = NumberedTraits([Attack()],[5])
        unit.traits["BlackMagic"] = NumberedTraits([GT.RangeAttack()],[5])
        #unit.traits["GenericTraits"] = {"Fireball":Fireball()}
        
        
        unit.attributes.hitpoints = 50        
        unit.attributes.damage = 5
        