from data.traits.generictraits import *
from tactics.util import *
#import data.traits.Generictraits as GT
from userinterface.Numberedtraits import *

from tactics.Move import *
from tactics.Attack import *
#from data.traits.GenericTrait import Move
class Unittypes(object):
    def FastFighter(self,unit):
        unit.attributes.speed = 3
        unit.attributes.hitpoints = 50        
        unit.attributes.damage = 50
        move = NumberedTraits([Move()],[5])
        unit.traits["Move"] = move
        attack = NumberedTraits([Attack()],[5])
        unit.traits["Attack"] = attack
                       
#    def SlowFighter(self,unit):
#        unit.attributes.speed = 5
#        unit.attributes.hitpoints = 50        
#        unit.attributes.damage = 50
        
    def Mage(self,unit):
        unit.attributes.speed = 4
        #dir(self)
        #dir(data)
        #dir(GT)
        move = NumberedTraits([Move()],[5])
        unit.traits["Move"] = move
        attack = NumberedTraits([Attack()],[5])
        unit.traits["Attack"] = attack
        
        range = NumberedTraits([RangeAttack()],[5])
        unit.traits["BlackMagic"] = range
        #unit.traits["GenericTraits"] = {"Fireball":Fireball()}
        
        
        unit.attributes.hitpoints = 50        
        unit.attributes.damage = 50
        