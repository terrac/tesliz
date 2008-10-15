from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *

class Unitdata(object):
    def terra(self,unit):
        buildUnit(unit,"Spark",3,"Player1")
        mental = Mind()
        mental.map={"combat":Combat(unit,action.Attack),"follower":Follower(unit)}
        setupExtra(unit,mental)
        
                       
    def matt(self,unit):
        buildUnit(unit,"Ta",3,"Player1")
        setupExtra(unit)
    
    def lina(self,unit):
        buildUnit(unit,"ZaiSoldier",3,"Player1")
        mental = Mind()
        mental.map={"combat":Combat(unit,action.Attack),"leader":Leader(unit,Ogre.Vector3(50,-20,0)),"conversation":Response(unit)}
        setupExtra(unit,mental)
        unit.node.getAttachedObject(0).setMaterialName( "Spark/SOLID" )
        
        unit.knowledgelist.insert(0,unit.getName())
        #unit.mental = Mind([Leader(unit),Fighter(unit)])
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        zai = {"kobold":["Fighter","Leader","GreenMage"]}
        vec = Ogre.Vector3(10,-20,0)
        vec2 = Ogre.Vector3(30,-20,0)
        #vec3 = Ogre.Vector3(-30,-20,0)
        vec4 = Ogre.Vector3(50,-20,0)
        s.event = EventPositions({vec:Event(zai,2,vec),vec2:Event(zai,3,vec2),vec4:Event(zai,4,vec4)})
        