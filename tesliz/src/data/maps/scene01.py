from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *
from tactics.createunits import *

class Unitdata(object):

    def Terra(self,unit):
        buildUnit(unit,"Squire","Human",5,"Player1")
        setupExtra(unit)
        unit.node.getAttachedObject(0).setMaterialName( "Spark/SOLID" )
        
    def Fiore(self,unit):
        #head bandit
        buildUnit(unit,"Squire","Human",5,"Computer1")
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
        CreateList(["Squire","Squire","Squire"],"Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(2,0,22),Ogre.Vector3(2,0,26)],[1,2,1])
        CreateList(["Squire","Squire","Squire"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
        terra = s.unitmap["Terra"]
        fiore = s.unitmap["Fiore"]
        #setup a map of units with turns and positions and add it on
        convo1 =[(terra,"We are surrounded"),
         (fiore,"Hail travelers we are bandits in need of money.  We will accept it the easy or the hard way"),
         (terra,"We haven't got any money.  We spent it all on goods"),
         (fiore,"Well I am afraid we don't accept goods other than gold, spices, or weapons.  You should really research your routes and know this stuff .  "),
         (fiore,"I am feeling generous today and I will accept an arm and a leg as payment for your lack of goods"),
         (terra,"I like my arms!"),
         (fiore,"Its your choice.")
         ]
        tmap = {0:convo1,"end":(terra,"We have won!"),"death-Fiore":(terra,"I bet you didn't expect that")}
        s.event = Event(turnmap = {terra:tmap})