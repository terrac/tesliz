#from tactics.Turn import Turn

import ogre.renderer.OGRE as Ogre
import logging
import os
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import winsound
import pygame.mixer
#import pygame.mixer_music





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
           
           
           pygame.mixer.init(48000,16)
           #self.soundset = set()
           #self.channelset = set()
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
           self.gridmap = None
           
        
        def removeUnit(self,unit):
            unit.destroy()

            #currently this causes problems if it is removed .  So I am not removingi it
            if unit.node:
                self.app.sceneManager.getRootSceneNode().removeChild(unit.node)
            unit.node = None   
            unit.body = None            
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
                s.event.endEvent()
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
#            if hasattr(self, "overviewmap"):                
            self.overviewmap.currentVisited("Player1")
#            else:
#                raise Exception("Not sure what to do here for edit mode yet")
#                self.overviewmap = Overviewmap
            #self.running = False
            
            
            
            
            
            
        def log(self,text,calling = None):
            text = str(text)
            sf.Application.debugText = text
            self.logger.info(text+ str(calling))                
            print text
        def screenshot(self):    
            self.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
        def playsound(self,filename="C:\sound.wav",directory ="media\\sounds\\",option = None):
            
            sound = pygame.mixer.Sound(directory+filename)
            sound.set_volume(s.settings.effectvolume)
            if option == "loop":
                sound.play(-1)
            else:
                sound.play()
            return sound
            #choose a desired audio format
             #raises exception on fail
            
            #sound = self.mixer.Sound("media\\sounds\\"+filename)
            #self.soundset.add(sound)
            
            #self.channelset.add(sound.play())
            
            #I can't figure this out and I really don't care
            winsound.PlaySound("media\\sounds\\"+filename, winsound.SND_FILENAME|winsound.SND_ASYNC)
        def playmusic(self,filename="C:\sound.wav"):
            #
            #pass
            try:
                pygame.mixer.music.load("media\\sounds\\"+filename)
                pygame.mixer.music.set_volume(s.settings.musicvolume)
                pygame.mixer.music.play()
            except Exception,e:
                self.log(e,self)
                
            
            #winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
    
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
        if isinstance(z, tuple):
            y += "("
            for w in z:
                y += str(w)
            y += ")"
        else:
            y += str(z)
    return y
def debugpickle(obj,tofind = Ogre.Vector3,depth = 0):
    print obj
    depth +=1
    if depth > 10:
        return
    if isinstance(obj, tofind):
        return obj
    if hasattr(obj, "__getstate__"):
        
        for x in obj.__getstate__().values():
            debugpickle(x,tofind,depth)
    elif hasattr(obj, "__dict__"):
        
        for x in obj.__dict__.values():
            debugpickle(x,tofind,depth)      
    elif hasattr(obj, "__iter__"):
        for x in obj:
            debugpickle(x, tofind,depth)  
    