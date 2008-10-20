#from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *
from data.races import *

s = Singleton()
class Settings(object):
    
    #playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":HumanPlayer()}
    def __init__(self):
        playermap = {"Player1":HumanPlayer("Player1"),"Computer1":ComputerPlayer("Computer1")}
        racemap = Races().map
        s.playermap = playermap
        s.racemap = racemap
        
        
        s.app.setTurnbased(True)
        s.AIon = True
        s.fog = True
        s.app.currentmap = 'scene01'
        s.app.World.setWorldSize(Ogre.Vector3(-100,-100,-100),Ogre.Vector3(100,100,100))
    
      
        