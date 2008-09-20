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
           if os.exists('tesliz.log'):
               os.remove('tesliz.log')
           
           hdlr = logging.FileHandler('tesliz.log')
#           formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
           formatter = logging.Formatter('%(message)s')
           hdlr.setFormatter(formatter)
           self.logger.addHandler(hdlr)
           self.logger.setLevel(logging.INFO)
           
           
        #key = name : value = node
        unitmap = dict()
        
        playermap= dict()
        actionlist= []
        turn = None
        framelistener = None
        app = None
        vector = Ogre.Vector3(0,0,0)
        turnbased = True
        ended = False
        event = None
        def removeUnit(self,unit):
            
            self.app.sceneManager.getRootSceneNode().removeChild(unit.node)
            unit.body = None
            del self.unitmap[unit.getName()]
            unit.player.unitlist.remove(unit)
            
            a = ""
            for e in unit.player.unitlist:
                a += str(e)
            self.log(str(unit) + " destroyed.  Unitlist"+str(len(unit.player.unitlist))+a)
            if len(unit.player.unitlist) == 0:
                self.log("endgame")
                self.endGame()
            del unit    
                
        def endGame(self):
            #sheet = CEGUI.WindowManager.getSingleton().getWindow("root_wnd")
            winMgr = CEGUI.WindowManager.getSingleton()
            list = winMgr.getWindow("QuitButton")
            #sheet.addChildWindow(list)
            list.setText("WINNER !!!!!")
            self.ended = True
            list.setPosition(CEGUI.UVector2(cegui_reldim(0.335), cegui_reldim(0.3)))
            list.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim(0.3)))
            list.setAlwaysOnTop(True)
            
        def log(self,text):
            sf.Application.debugText = str(text)
            self.logger.info(text)                
            print text
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
