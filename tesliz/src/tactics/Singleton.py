#from tactics.Turn import Turn

import ogre.renderer.OGRE as Ogre
import logging
import os
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import winsound
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
           self.running = True
           self.event = None
           self.reset()
           
        #key = name : value = node
        def reset(self):
            self.unitmap = dict()            
            self.playermap= dict()
            self.actionlist= []
            self.cplayer = None
            
        
        def removeUnit(self,unit):
            
            self.app.sceneManager.getRootSceneNode().removeChild(unit.node)
            unit.body = None
            del self.unitmap[unit.getName()]
            unit.player.unitlist.remove(unit)
            
            a = ""
            for e in unit.player.unitlist:
                a += str(e)
            self.log(str(unit) + " destroyed.  Unitlist"+str(len(unit.player.unitlist))+a)
            if not unit.player.unitlist:
                self.log("endgame")
                self.endGame()
            
            unit.destroy()    
            del unit    
            
                
        def endGame(self):
          
            #sheet = CEGUI.WindowManager.getSingleton().getWindow("root_wnd")
            if s.event:
                s.event.end()
            winMgr = CEGUI.WindowManager.getSingleton()
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
            self.running = False
            
            self.reset()
            
            
        def log(self,text,calling = None):
            text = str(text)
            sf.Application.debugText = text
            self.logger.info(text+ str(calling))                
            print text+ str(calling)
        def screenshot(self):    
            self.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
        def playsound(self,filename="C:\sound.wav"):
            winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC)
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