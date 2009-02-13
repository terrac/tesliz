from tactics.OverviewMap import Position
from tactics.OverviewMap import AddDifferentPos
from tactics.Singleton import *
import tactics.util
def setupDefaultPositions(overviewmap):
    overviewmap.root =pos = Position((0,7,0),"Linder",False)
    pos1 = Position((5,7,0),"Exalia")
    pos.next = pos1
    
    
    #pos1.next = Position((5,7,5),"scene02")
    pos1.next = AddDifferentPos((overviewmap.root,Position((5,7,5),"Lindenberry")))
    overviewmap.cpos = overviewmap.root
    
    overviewmap.placetoscene = {"Linder":"linderenter","Linder-Exit":"linderexit","Exalia":"exalia",}
    if not s.test:
        tactics.util.buildUnitNoNode("Alluvia","Player1", "Wizard",2)
        
    s.playermap["Player1"].items.add("Potion")
    s.playermap["Player1"].items.add("Potion")
    s.playermap["Player1"].items.add("Potion")
    s.playermap["Player1"].items.add("Potion")
    s.playermap["Player1"].items.add("Potion")
    
    s.playermap["Player1"].items.add("LeatherArmor")