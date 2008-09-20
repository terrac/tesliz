from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *

class Unitdata(object):
    def bandit2(self,unit):
        buildUnit(unit,"FastFighter",5,"Computer1")
        
                       
    def bandit1(self,unit):
        buildUnit(unit,"FastFighter",5,"Computer1")
        
    
    def lina(self,unit):
        buildUnit(unit,"Spark",5,"Player1")

        unit.mental = Mind([Leader(unit),Fighter(unit)])
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)
    def setupEvents(self):
        vec = Ogre.Vector3(0,-20,0)
        s.event = EventPositions({vec:Event("Zai",5,vec)})  
        from tactics.Event import *          