from tactics.util import *

class Unitdata(object):
    def horf2(self,unit):
        buildUnit(unit,"FastFighter","Computer1","horf")
        buildPhysics(unit)
                       
    def horf1(self,unit):
        buildUnit(unit,"FastFighter","Computer1","horf")
        buildPhysics(unit)
    
    def anti1(self,unit):
        buildUnit(unit,"Mage","Player1","Materiala")
        buildPhysics(unit)
    
    def anti2(self,unit):
        buildUnit(unit,"Mage","Player1","anti")
        buildPhysics(unit)
        
    def anti3(self,unit):
        buildUnit(unit,"Mage","Player1","anti")
        buildPhysics(unit)        
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)            