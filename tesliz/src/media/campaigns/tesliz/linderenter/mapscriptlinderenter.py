from tactics.util import *

from tactics.Event import *
from tactics.createunits import *
 
import utilities.FollowCamera
import ogre.renderer.OGRE as Ogre
import data.executables.playsound

class EndGame:
    def execute(self,timer):
        s.endGame()
        s.app.setTurnbased(True)
        
        
def addScripts(scriptmap,current= None):
   
    #alluvia =tactics.util.buildUnitNoNode("Alluvia","Player1", "Wizard")
    SetupPlayer("Player1",[Ogre.Vector3(0,0,0)])
    girl1 =tactics.util.buildUnitNoNode("girl1", "Computer1","Squire")
    girl2 =tactics.util.buildUnitNoNode("girl2", "Computer1","Squire")
    merchant =tactics.util.buildUnitNoNode("merchant", "Computer1","Squire")
    cerc =tactics.util.buildUnitNoNode("cerc", "Computer1","Squire")
    SetupPlayer("Computer1",[Ogre.Vector3(-15,0,3),Ogre.Vector3(-15,0,4),Ogre.Vector3(1,0,0),Ogre.Vector3(7,0,2)])
    #CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,3)],[1,2,1])
#    alluvia = s.unitmap["Alluvia"]
#    cerc = s.unitmap["cerc"]
#    girl1 = s.unitmap["girl1"]
#    girl2 = s.unitmap["girl2"]
#    merchant = s.unitmap["merchant"]
#        fiore = s.unitmap["Fiore"]
    #setup a map of units with turns and positions and add it on
    
    
    #AttachCamera(girl1).execute()
    girlconvo =ScriptEvent([
    (girl1,"Waiting for everything to load",5.5),
    utilities.FollowCamera.FollowCamera(girl1),
    
                            data.traits.basictraits.FFTMove(girl1,Ogre.Vector3(13,0,3),.5),
             data.traits.basictraits.FFTMove(girl2,Ogre.Vector3(13,0,4),.5),
    data.executables.playsound.PlaySound(s.currentdirectory+"linderenterconvo1.ogg"),         
             (girl1,"Did you see that Belouve boy fighting?  Hes a cutie",3.1),
     (girl2,"Personally I don't know how you can talk about the Belouves like that.  They have ruined this town.",4.6),
     (girl1,"Aww, youre no fun",1.5),
     (girl2,"Did you see the price of cloth today?  The old Ratsger said that the Siege's kid left the door open on their barn and ruined half their supply",7.9),
     (girl1,"Yeah, Im not buying any cloth till the price goes down",3.35),
     #AttachCamera(cerc),
     
     (cerc,"I'll show them today what kind of man I am",2.4),
     utilities.FollowCamera.FollowCamera(cerc),
     data.traits.basictraits.FFTMove(cerc,Ogre.Vector3(0,0,2)),
     (cerc,""),
     data.executables.playsound.PlaySound(s.currentdirectory+"linderenterconvo2.ogg"),
     (cerc,"Whats this, a transaction going on in broad daylight without my approval? What do you think i am? A chump?",6.2),
     
     (cerc,"To do business here you have to pay the toll.",2.4),
     (merchant,"Ignore him.  I feel sorry for him as he is Allison's boy, but he is going a bit too far now",5.9),
     (cerc,"I am going to be big in this town someday.  You will need my protection like you did in the war!",6),
     #(alluvia,"No"),
#         (cerc,"No?"),
#         (cerc,"Well I wish you good luck with that attitude my friend"),
   
     EndGame()
     ],None,Unit())
    z = ""
    for x in girlconvo.tlist:
        if isinstance(x, tuple):
            for y in x:
                if isinstance(y, str):
                    z += y +" "
    print z
    convo1 =[
     girlconvo,
     (merchant,"The recent downturn in the economy due to all the soldiers coming back from the war with no jobs has cost me a lot.  They are all thieves now!"),
     (merchant,"I can offer no more than $grain-price$ gold for your $grain$."),
     
      
     ]
    
    s.app.msnCam.setOrientation(Ogre.Quaternion(-1,0,0,0))
    s.app.setTurnbased(False)
    s.framelistener.pauseturns = True
    
    s.playmusic("mozk47.mid")
    scriptmap["start"] = convo1
    
    
