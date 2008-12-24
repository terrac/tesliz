from tactics.util import *

from tactics.Event import *
from tactics.createunits import *

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
        
        
        
        #unit =buildUnitNoNode("Alluvia","Player1", "Squire")
        unit =buildUnitNoNode("Oath","Player1", "Squire")
        #unit =buildUnitNoNode("Bahaullah","Player1", "Squire")
        #unit =buildUnitNoNode("Boru","Player1", "Squire")
        SetupPlayer("Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(0,0,19)])
        
        CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
        alluvia = s.unitmap["Alluvia"]
        fiore = s.unitmap["Fiore"]
        #setup a map of units with turns and positions and add it on
        convo1 =[(alluvia,"We are surrounded"),
         (fiore,"Hail travelers we are bandits in need of money.  We will accept it the easy or the hard way"),
         (alluvia,"We haven't got any money.  We spent it all on goods"),
         (fiore,"Well I am afraid we don't accept goods other than gold, spices, or weapons.  You should really research your routes and know this stuff .  "),
         (fiore,"I am feeling generous today and I will accept an arm and a leg as payment for your lack of goods"),
         (alluvia,"I like my arms!"),
         (fiore,"Its your choice.")
         ]
        tmap = {0:convo1,'end':(alluvia,"We have won!")}
        fmap = {'death-Fiore':(alluvia,"I bet you didn't expect that")}
        s.event = Event(turnmap = {alluvia:tmap,fiore:fmap})