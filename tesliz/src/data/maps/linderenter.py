from tactics.util import *

from tactics.Event import *
from tactics.createunits import *
import tactics.Move

class EndGame:
    def execute(self,timer):
        s.endGame()
        #s.app.setTurnbased(True)

class AttachCamera:
    def __init__(self, node,position = Ogre.Vector3(0,0,0)):
        if isinstance(node, Unit):
            node = node.node
        self.node = node
        self.position = position
    def execute(self,timer= None):
        #s.app.msnCam.getParent().removeChild(s.app.msnCam)
        s.app.msnCam.detachAllObjects()
        self.node.attachObject(s.app.camera)
        #self.node.addChild(s.app.msnCam)
        #s.app.msnCam.setPosition(self.position)
        #s.app.setTurnbased(True)
        
class Unitdata(object):

    
    def Fiore(self,unit):
        #head bandit
        buildUnit(unit,"Squire","Human",2,"Computer1")
        setupExtra(unit)
        #unit.node.getAttachedObject(0).setMaterialName( "Spark/SOLID" )

    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        #unit.node.setScale(Ogre.Vector3(5,5,5))
        
        buildImmoblePhysics(unit)  
    def setupEvents(self):
        #ulist = ["Chemist"]
        #CreateRandom(ulist,"Player1",Ogre.Vector3(9,-25,4))
        #CreateRandom(ulist,"Computer1",Ogre.Vector3(20,-25,4))
        #CreateList(["Chemist","Chemist","Chemist"],"Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(2,0,22),Ogre.Vector3(2,0,26)],[1,2,1])
        
        
        tactics.util.buildUnitNoNode("Alluvia","Player1", "Wizard")
#        unit =buildUnitNoNode("Alluvia","Player1", "Squire")
       
        #unit =buildUnitNoNode("Bahaullah","Player1", "Squire")
        #unit =buildUnitNoNode("Boru","Player1", "Squire")
        SetupPlayer("Player1",[Ogre.Vector3(2,0,19)])
        
        girl1 =tactics.util.buildUnitNoNode("girl1", "Computer1","Squire")
        girl2 =tactics.util.buildUnitNoNode("girl2", "Computer1","Squire")
        merchant =tactics.util.buildUnitNoNode("merchant", "Computer1","Squire")
        cerc =tactics.util.buildUnitNoNode("cerc", "Computer1","Squire")
        
        #theres probably a better solution for this
        #narrator =tactics.util.buildUnitNoNode("narrator", "Computer1","Squire")
        
        SetupPlayer("Computer1",[Ogre.Vector3(-12,0,19),Ogre.Vector3(-12,0,20),Ogre.Vector3(4,0,19),Ogre.Vector3(20,0,19)])
        #CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
        alluvia = s.unitmap["Alluvia"]
#        fiore = s.unitmap["Fiore"]
        #setup a map of units with turns and positions and add it on
        s.app.setTurnbased(False)
        
        AttachCamera(girl1).execute()
        girlconvo =ScriptEvent([
                                tactics.Move.FFTMove(girl1,Ogre.Vector3(50,0,17),.5),
                 tactics.Move.FFTMove(girl2,Ogre.Vector3(50,0,18),.5),
                 
                 (girl1,"Did you see that Belouve boy fighting?  Hes a cutie"),
         (girl2,"Personally I don't know how you can talk about the Belouves like that.  They have ruined this town."),
         (girl1,"Aww, youre no fun"),
         (girl2,"Did you see the price of cloth today?  The old Ratsger said that the Siege's kid left the door open on their barn and ruined half their supply"),
         (girl1,"Yeah, Im not buying any cloth till the price goes down"),
         AttachCamera(cerc),
         (cerc,"I'll show them today what kind of man I am"),
         tactics.Move.FFTMove(cerc,Ogre.Vector3(0,0,20)),
         (cerc,"Hey"),
         (cerc,"Whats this, a transaction going on in broad daylight without my approval? What do you think i am? A chump?"),
         
         (cerc,"To do business here you have to pay the toll."),
         (merchant,"Ignore him"),
         (alluvia,"No"),
         (cerc,"No?"),
         (cerc,"Well I wish you good luck with that attitude my friend"),
         EndGame()
         ],Unit())
        
        convo1 =[
         girlconvo,
         (merchant,"The recent downturn in the economy due to all the soldiers coming back from the war with no jobs has cost me a lot.  They are all thieves now!"),
         (merchant,"I can offer no more than $grain-price$ gold for your $grain$."),
         
          
         ]
        tmap = {0:convo1 }
        
        s.event = Event(turnmap = {alluvia:tmap})
        
    def setupTestMap(self):
        pass