from tactics.util import *

from tactics.Event import *
from tactics.createunits import *

def addScripts(scriptmap):
        
    oath =buildUnitNoNode("Oath","Player1", "Knight")
    
    SetupPlayer("Player1",[Ogre.Vector3(0,0,5),Ogre.Vector3(0,0,6)])
    cerc =tactics.util.buildUnitNoNode("cerc", "Computer1","Squire")
    trent  =tactics.util.buildUnitNoNode("trent", "Computer1","Squire")
    SetupPlayer("Computer1",[Ogre.Vector3(5,0,5),Ogre.Vector3(5,0,6)])
    #CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
    alluvia = s.unitmap["Alluvia"]

    #fiore = s.unitmap["Fiore"]
    #setup a map of units with turns and positions and add it on
    convo1=ScriptEvent([
     (cerc,"Fancy surrounding you here",1.8),
     (alluvia,"You again",1),
     (cerc,"I have a reputation to maintain",2.2),
     (oath,"Wait did I miss something?",1.7),
     (cerc,"Who are you?",1),
     (oath,"I am the leader and I have the decency to not get thieves after us",3.7),
     (alluvia,"Well sorry, I was just checking the price to see our pay",3.4),
     (oath,"You could have mentioned something",1.7),
     (alluvia,"I can't be expected to remember everything",2.5),
     (cerc,"Hey hey, you can continue this conversation after you are dead.  Me and trent will make short work of you",6.5)
      
     ],"convo")
    s.playmusic("k339_1.mid")
    scriptmap["start"] = convo1
    
        #tmap = {0:convo1}

#        fmap = {'death-Cerc':(alluvia,"Wut Wut")}
#        s.event = Event(turnmap = {cerc:fmap}, startlist = convo1)
        
            
        
def setupTestMap():
    tactics.util.buildUnitNoNode("Alluvia","Player1", "Wizard",2)
    del s.overviewmap.placetoscene["Linder-Exit"]
#        unit =buildUnitNoNode("Alluvia","Player1", "Wizard",2)
       
