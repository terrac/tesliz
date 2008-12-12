#from tactics.Turn import Turn

import ogre.renderer.OGRE as Ogre
import logging
import os
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import winsound

class LoadScene:
    def __init__(self,name):
        self.name = name
    def execute(self,timer):
        s.app.loadScene(self.name)        

class Singleton:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """
        def __init__(self):
           self.logger = logging.getLogger('myapp')
           if os.path.exists('tesliz.log'):
               os.remove('tesliz.log')
           
           hdlr = logging.FileHandler('tesliz.log')
#           formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
           formatter = logging.Formatter('%(message)s')
           hdlr.setFormatter(formatter)
           self.logger.addHandler(hdlr)
           self.logger.setLevel(logging.INFO)
           self.turn = None
           self.framelistener = None
           self.app = None
           self.turnbased = True
           
           #makes things based on timesincelast frame move faster or slower
           self.speed = 1
           #current player for functions like changing jobs 
           self.cplayer = None
           
           # BPC - TEMP data for developing job stuff
           #self
           
           #self.running = True
           self.event = None
           self.playermap= dict()
           
           self.unitmap = dict()
           # state variable saying whether CEGUI has been initialized or not, default None (False)
           self.initCEGUI = None
           
        
        def removeUnit(self,unit):
            unit.destroy()   
            self.app.sceneManager.getRootSceneNode().removeChild(unit.node)
            del self.unitmap[unit.getName()]
            
            #units now always stay with players and can be ressurected.  But they can still be dismissed
            #unit.player.unitlist.remove(unit)
            unit.node = None
            a = ""
            liveunits = 0
            for e in unit.player.unitlist:
                a += str(e)
                if e.node:
                    liveunits +=1
            self.log(str(unit) + " destroyed.  Unitlist"+str(len(unit.player.unitlist))+a)
            if not liveunits:
                self.log("endgame")
                self.endGame()
            
                   
            
                
        def endGame(self):
            for unit in self.unitmap.values():
                unit.destroy()
            if s.event:
                s.event.end()
            del self.playermap["Computer1"]
            #sheet = CEGUI.WindowManager.getSingleton().getWindow("root_wnd")

            
            winMgr = CEGUI.WindowManager.getSingleton()
            name = "QuitButton"
            if winMgr.isWindowPresent(name):            
                window = winMgr.getWindow(name)
            else:
                window = None
            #sheet.addChildWindow(list)
            for x in self.unitmap.values():
                if window:                
                    window.setText(x.player.name+" WINNER !!!!!")
                    window.setPosition(CEGUI.UVector2(cegui_reldim(0.335), cegui_reldim(0.3)))
                    window.setSize(CEGUI.UVector2(cegui_reldim(0.3), cegui_reldim(0.1)))
                    window.setAlwaysOnTop(True)
                #losing should reload from file                
                
                
                
                break;
            self.overviewmap.currentVisited("Player1")
            
            #self.running = False
            
            
            
            
            
            
        def log(self,text,calling = None):
            text = str(text)
            sf.Application.debugText = text
            self.logger.info(text+ str(calling))                
            print text
        def screenshot(self):    
            self.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
        def playsound(self,filename="C:\sound.wav"):
            winsound.PlaySound("media\\sounds\\"+filename, winsound.SND_FILENAME|winsound.SND_ASYNC)
        def playmusic(self,filename="C:\sound.wav"):
            winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
    
    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Singleton.__instance is None:
            # Create and remember instance
            Singleton.__instance = Singleton.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = Singleton.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
s = Singleton()

def printlist(x):
    y = ""
    for z in x:
        y += str(z)
    return y
