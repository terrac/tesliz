from tactics.util import *

from tactics.Event import *
from tactics.createunits import *
 


class ChangeSides:
    def __init__(self,unit,player):
        self.unit = unit
        self.player = player
    def execute(self,timer):
        self.unit.player.unitlist.remove(self.unit)
        self.unit.player = self.player
        if hasattr(self.player, "setVisualMarker"):
            self.player.setVisualMarker(self.unit)
        s.app.setTurnbased(True)


  
    
        
        #unit.node.setScale(Ogre.Vector3(5,5,5))
    
      
def addScripts(scriptmap):
    
    #ulist = ["Chemist"]
    #CreateRandom(ulist,"Player1",Ogre.Vector3(9,-25,4))
    #CreateRandom(ulist,"Computer1",Ogre.Vector3(20,-25,4))
    #CreateList(["Chemist","Chemist","Chemist"],"Player1",[Ogre.Vector3(2,0,19),Ogre.Vector3(2,0,22),Ogre.Vector3(2,0,26)],[1,2,1])
    
    
    
#        unit =buildUnitNoNode("Alluvia","Player1", "Squire")
   
    #unit =buildUnitNoNode("Bahaullah","Player1", "Squire")
    #unit =buildUnitNoNode("Boru","Player1", "Squire")
    SetupPlayer("Player1",[Ogre.Vector3(-4,0,11),Ogre.Vector3(13,0,12)])
    
    fighter1 =tactics.util.buildUnitNoNode("fighter1", "Computer1","Knight")
    fighter2 =tactics.util.buildUnitNoNode("fighter2", "Computer1","Knight")
    balla =tactics.util.buildUnitNoNode("balla", "Computer1","Poet")
    
    
    #theres probably a better solution for this
    #narrator =tactics.util.buildUnitNoNode("narrator", "Computer1","Squire")
    
    SetupPlayer("Computer1",[Ogre.Vector3(-12,0,12),Ogre.Vector3(-12,0,13),Ogre.Vector3(-10,0,12)])
    #CreateList(["Squire","Squire","Chemist"],"Computer1",[Ogre.Vector3(-18,0,17),Ogre.Vector3(14,0,18),Ogre.Vector3(12,0,20)],[1,2,1])
    alluvia = s.unitmap["Alluvia"]
    oath = s.unitmap["Oath"]
#        fiore = s.unitmap["Fiore"]
    #setup a map of units with turns and positions and add it on
    #s.app.setTurnbased(False)
    

    
    convo1 =[
        data.traits.basictraits.FFTMove(balla,Ogre.Vector3(12,0,9),.45),
         data.traits.basictraits.FFTMove(fighter1,Ogre.Vector3(12,0,10),.45),
          data.traits.basictraits.FFTMove(fighter2,Ogre.Vector3(11,0,10),.45),
             
             (balla,"You will never catch me!"),
     (balla,"Yoink (you might feel that your purse is a bit lighter)"),
     (alluvia,"Hey you come back here"),
      data.traits.basictraits.FFTMove(alluvia,Ogre.Vector3(11,0,12),.5),
     (fighter1,"Now theres someone with a serious kleptomania problem"),
     (fighter2,"I feel undervalued.  Did she not think that us chasing her was enough?"),
     (balla,"Hey Oath, wanna help me fight for this bag of gil I just got?"),
     (oath,"Sure"),
     (fighter1,"Ha, 2 against 3.  You made more enemies than friends"),
     (alluvia,"Actually I'm with oath"),
     (fighter2,"Wait, what?"),
      ChangeSides(balla,s.playermap["Player1"])
     ]
#    import os
#    unitmap = {fighter1:"en\\en-sc+m3",fighter2:"en\\en-sc+m2",alluvia:"en\\en-sc+f3",oath:"en\\en-wm+f3",balla:"en\\en-n+f3"}
#    name = "convo"
#    y = 1
#    for x in convo1:
#        if isinstance(x, tuple):
#            toex = 'C:\\eclipse\\eSpeak\\espeak.exe -w C:\\eclipse\\eSpeak\\'+name+str(y)+'.wav -a 50 -v '+unitmap[x[0]]+' "'+x[1]+'"'
#            os.system(toex)
#            print toex
#            y +=1

    end =[
             (alluvia,"So, what was this all about?"),
             (balla,"I am friends with Oath and apparently so are you.  Sorry about taking your money"),
     (balla,"Anyways that was a fortuituous event"),
     
      
     (balla,"Those two had been hunting me for a week"),
     (balla,"I was about to leave the city"),
     (alluvia,"Its no problem.  Say, we need a third person.  If you still want to leave the city you are free to come with us"),
     (balla,"Sure, give me a couple hours to clean up"),
     (oath,"Hey, I don't know if we should be hanging around with such unsavoury types"),
     (balla,"Well you are stuck with me now"),

     ]
    scriptmap["start"] = ScriptEvent(convo1,"convo")
    scriptmap["end"] = end
    
    
#    s.event = Event(tmap)
    
def setupTestMap():
    
    unit =buildUnitNoNode("Alluvia","Player1", "Wizard",2)
    unit =buildUnitNoNode("Oath","Player1", "Knight",2)