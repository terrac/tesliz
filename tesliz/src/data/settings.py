#from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *

s = Singleton()
class Settings(object):
    playermap = {"Player1":HumanPlayer("Player1"),"Computer1":ComputerPlayer("Computer1")}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":HumanPlayer()}
    def __init__(self):
        s.app.setTurnbased(True)
        s.fog = True
        s.app.currentmap = 'scene01'
        s.app.World.setWorldSize(Ogre.Vector3(-100,-100,-100),Ogre.Vector3(100,100,100))
    
      
        