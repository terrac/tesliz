from tactics.util import *

from tactics.Event import *
from tactics.createunits import *

class Unitdata(object):

    

    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        #unit.node.setScale(Ogre.Vector3(5,5,5))
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        
        
        SetupPlayer("Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(0,0,19)])
        cerc =tactics.util.buildUnitNoNode("cerc", "Computer1","Squire")
        SetupPlayer("Computer1",[Ogre.Vector3(-20,0,19)])
        CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
        alluvia = s.unitmap["Alluvia"]
        oath =buildUnitNoNode("Oath","Player1", "Squire")
        #fiore = s.unitmap["Fiore"]
        #setup a map of units with turns and positions and add it on
        convo1 =[
         (cerc,"Fancy surrounding you here"),
         (alluvia,"You again"),
         (cerc,"I have a reputation to maintain"),
         (oath,"Wait did I miss something?"),
         (cerc,"Who are you?"),
         (oath,"I am the leader and I have the decency to not get thieves after us"),
         (alluvia,"Well sorry, I was just checking the price to see our cut"),
         (oath,"You could have mentioned something"),
         (alluvia,"I can't be expected to remember everything"),
         (cerc,"Hey hey, you can continue this conversation after you are dead"),
         ]
        tmap = {0:convo1}
        fmap = {'death-Cerc':(alluvia,"Wut Wut")}
        s.event = Event(turnmap = {alluvia:tmap,cerc:fmap})