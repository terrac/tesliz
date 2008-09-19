#from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *
from tactics.Event import *
s = Singleton()
class Settings(object):
    #playermap = {"Player1":HumanPlayer(),"Computer1":ComputerPlayer()}
    playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":HumanPlayer()}
    def __init__(self):
        s.turnbased = True
        s.fog = False
        s.app.currentmap = 'scene01'
        s.app.World.setWorldSize(Ogre.Vector3(-100,-100,-100),Ogre.Vector3(100,100,100))
        vec = Ogre.Vector3(0,-20,0)
        s.event = EventPositions({vec:Event("Zai",5,vec)})
        