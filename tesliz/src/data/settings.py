#from tactics.util import *
from tactics.Player import *
from tactics.Singleton import *
import ogre.gui.CEGUI as CEGUI
from tactics.OverviewMap import Position
import tactics.util

s = Singleton()
class Settings(object):
    
    #playermap = {"Player1":ComputerPlayer(),"Computer1":ComputerPlayer()}
    #playermap = {"Player1":ComputerPlayer(),"Computer1":HumanPlayer()}
    
    def setupPlayerMap(self):
        playermap = {"Player1":HumanPlayer("Player1")}        
        s.playermap = playermap        
        s.cplayer = playermap["Player1"]
    def __init__(self):
        self.setupPlayerMap()
        s.settings = self
        
        s.app.setTurnbased(True)
        s.AIon = True
        #s.AIon = False
        self.musicvolume = .1
        self.effectvolume = 1
        s.fog = False
        s.app.currentmap = 'scene01'
        s.app.World.setWorldSize(Ogre.Vector3(-100,-100,-100),Ogre.Vector3(100,100,100))
        s.eventpausing = False
        s.speed = 111
        s.testspeed = 50
        #.damagemultiplier = 50
        s.damagemultiplier = 1
        
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
        self.scriptsetsunitdata = True
        self.scriptsetsunitpositions = False
#        s.eventpausing = True    
    def textChangedHandler(self, e):
        try:
            s.speed = int(str(e.window.getText()))
        except:
            e.window.setText(str(s.speed))
        return True    
    def handleAIONChange(self, e):
        s.AIon = not s.AIon
        e.window.setText(str(s.AIon)) 
        
        return True    
    def setupDefaultPositions(self,overviewmap):
        mod =__import__("media.campaigns."+s.campaignname+".settings")
        
        getattr(mod.campaigns,s.campaignname).settings.setupDefaultPositions(overviewmap)
        #tactics.util.buildUnitNoNode("Oath","Player1", "Squire")
#        tactics.util.buildUnitNoNode("Bahaullah","Player1", "Squire")
#        tactics.util.buildUnitNoNode("Boru","Player1", "Squire")
    
            