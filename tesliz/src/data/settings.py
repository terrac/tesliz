from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *
s = Singleton()
class Settings(object):
    #playermap = {"Player1":HumanPlayer(),"Computer1":ComputerPlayer()}
    playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    
    def __init__(self):
        s.turnbased = True
        s.app.currentmap = 'antimony'