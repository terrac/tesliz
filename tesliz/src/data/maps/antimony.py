from tactics.util import *

class Unitdata(object):
    def horf2(self,unit):
        buildUnit(unit,"FastFighter","Computer1","Red/SOLID")
        buildPhysics(unit)
                       
    def horf1(self,unit):
        buildUnit(unit,"FastFighter","Computer1","Red/SOLID")
        buildPhysics(unit)
    
    def anti1(self,unit):
        buildUnit(unit,"Mage","Player1","LightGreen/SOLID")
        buildPhysics(unit)
    
    def anti2(self,unit):
        buildUnit(unit,"Mage","Player1","LightGreen/SOLID")
        buildPhysics(unit)
        
    def anti3(self,unit):
        buildUnit(unit,"Mage","Player1","LightGreen/SOLID")
        buildPhysics(unit)        
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)            