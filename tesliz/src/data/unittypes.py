from tactics.util import *
from data.traits.BlackMagic import *
class Unittypes(object):
    def FastFighter(self,unit):
        unit.attributes.speed = 4
                       
    def SlowFighter(self,unit):
        unit.attributes.speed = 5
        
    def Mage(self,unit):
        #unit.attributes.speed = 3
        unit.traits["BlackMagic"] = {"Fireball":Fireball()}        
        