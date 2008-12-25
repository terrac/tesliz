from tactics.util import *

from tactics.Event import *
from tactics.createunits import *

def addScripts(scriptmap):
        
    oath =buildUnitNoNode("Oath","Player1", "Squire")
    
    SetupPlayer("Player1",[Ogre.Vector3(0,0,5),Ogre.Vector3(0,0,6)])
    cerc =tactics.util.buildUnitNoNode("cerc", "Computer1","Squire")
    trent  =tactics.util.buildUnitNoNode("trent", "Computer1","Squire")
    SetupPlayer("Computer1",[Ogre.Vector3(5,0,5),Ogre.Vector3(5,0,6)])
    #CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
    alluvia = s.unitmap["Alluvia"]

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
     (cerc,"Hey hey, you can continue this conversation after you are dead.  Me and trent will make short work of you")
      
     ]
    scriptmap["Script1"] = convo1
        #tmap = {0:convo1}

#        fmap = {'death-Cerc':(alluvia,"Wut Wut")}
#        s.event = Event(turnmap = {cerc:fmap}, startlist = convo1)
        
            
        
    def setupTestMap(self):
        pass
#        unit =buildUnitNoNode("Alluvia","Player1", "Wizard",2)
       
