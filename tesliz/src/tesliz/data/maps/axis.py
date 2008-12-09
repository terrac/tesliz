from tactics.util import *

class Unitdata(object):
    def axis2(self,unit):
        buildUnit(unit,"FastFighter","Player1")
        buildPhysics(unit)
                       
    def axis(self,unit):
        buildUnit(unit,"SlowFighter","Computer1","Red/SOLID")
        buildPhysics(unit)
    
    def axis3(self,unit):
        buildUnit(unit,"Mage","Player1","LightGreen/SOLID")
        buildPhysics(unit)
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)            