from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *
from tactics.CreateRandom import *

class Unitdata(object):

    def Terra(self,unit):
        buildUnit(unit,"Chemist","Human",5,"Player1")


        setupExtra(unit)
        unit.node.getAttachedObject(0).setMaterialName( "Spark/SOLID" )
        
        unit.knowledgelist.insert(0,unit.getName())
        #unit.mental = Mind([Leader(unit),Fighter(unit)])
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        ulist = ["Chemist"]

        CreateRandom(ulist,"Player1",s.gridmap.getOff(0,0).pos)
        CreateRandom(ulist,"Computer1",s.gridmap.getOff(1,0).pos)