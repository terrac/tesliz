from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *

class Unitdata(object):
    def bandit2(self,unit):
        buildUnit(unit,"FastFighter",1,"Player1")
        setupExtra(unit)
        
                       
    def bandit1(self,unit):
        buildUnit(unit,"FastFighter",1,"Computer1")
        setupExtra(unit)
    
    def lina(self,unit):
        buildUnit(unit,"Spark",5,"Player1")
        mental = Mind()
        mental.map={"combat":Combat(unit,action.Attack),"leader":Leader(unit)}
        setupExtra(unit,mental)
        #unit.mental = Mind([Leader(unit),Fighter(unit)])
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        zai = ["Spark","ZaiSoldier"]
        vec = Ogre.Vector3(10,-20,0)
        vec2 = Ogre.Vector3(30,-20,0)
        #vec3 = Ogre.Vector3(-30,-20,0)
        vec4 = Ogre.Vector3(50,-20,0)
        s.event = EventPositions({vec:Event(zai,2,vec),vec2:Event(zai,3,vec2),vec4:Event(zai,4,vec4)})
        