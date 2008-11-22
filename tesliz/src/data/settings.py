#from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *
from data.races import *
import ogre.gui.CEGUI as CEGUI

s = Singleton()
class Settings(object):
    
    #playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":HumanPlayer()}
    
    def setupPlayerMap(self):
        playermap = {"Player1":HumanPlayer("Player1"),"Computer1":ComputerPlayer("Computer1")}        
        s.playermap = playermap        
        s.cplayer = playermap["Player1"]
    def __init__(self):
        self.setupPlayerMap()
        racemap = Races().map
        s.racemap = racemap
        s.settings = self
        
        s.app.setTurnbased(True)
        s.AIon = True
#        s.AIon = False
        s.fog = False
        s.app.currentmap = 'scene01'
        s.app.World.setWorldSize(Ogre.Vector3(-100,-100,-100),Ogre.Vector3(100,100,100))
        s.eventpausing = False
        s.speed = 12
        
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "aion")
        CEGUI.System.getSingleton().getGUISheet().addChildWindow(btn)
        btn.setText(str(s.AIon))
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.7), cegui_reldim( 0.0)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleAIONChange")
        
        
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Editbox", "speed")        
        CEGUI.System.getSingleton().getGUISheet().addChildWindow(btn)
        btn.setText(str(s.speed))
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.8), cegui_reldim( 0.0)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        btn.subscribeEvent(CEGUI.Window.EventTextChanged,self, "textChangedHandler")
        
#        s.eventpausing = True    
    def textChangedHandler(self, e):
    
        s.speed = int(str(e.window.getText()))
        
        return True    
    def handleAIONChange(self, e):
        s.AIon = not s.AIon
        e.window.setText(str(s.AIon)) 
        
        return True    
            