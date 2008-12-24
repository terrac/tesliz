from tactics.util import *
from tactics.createunits import *
from tactics.Singleton import *

class Unitdata(object):
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        
        s.playermap["Player1"].items.addItem("Potion")
        
        SetupPlayer("Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(2,0,22),Ogre.Vector3(2,0,26),Ogre.Vector3(5,0,26)])
        
        CreateList(["Squire","Chemist","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])


    def setuptestmap(self):
        unit =buildUnitNoNode("Alluvia","Player1", "Chemist",2)
        unit =buildUnitNoNode("Oath","Player1", "Squire",1)
        unit =buildUnitNoNode("Bahaullah","Player1", "Squire",2)
        unit =buildUnitNoNode("Boru","Player1", "Squire",1)