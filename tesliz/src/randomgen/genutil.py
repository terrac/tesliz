import tactics.util
from tactics.Singleton import *

def Characters(Characters = "fighter",Ability = ["Attack"],Player ="Player1" ,Position = (0,0,0),Name = None,Level = 1):
    if not Name:
        Name = s.app.getUniqueName()
    tactics.util.buildUnitNoNode(Name, Player, Characters, Level)
    
    
