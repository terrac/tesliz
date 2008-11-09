# File: startMenu.py
# Brian Caines
# This starts the main menu

import ogre.renderer.OGRE as Ogre
import ogre.io.OIS as OIS
from utilities.BasicFrameListener import *     # a simple frame listener that updates physics as required..
from utilities.CEGUIFrameListener import *
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.gui.CEGUI as CEGUI

class MainMenuGUI (sf.Application):
    
    currentmap=None
    def __init__ ( self):
        sf.Application.__init__(self)
        
#        sf.Application.debugText = "aeou"

    def __del__ (self):
        del self.camera
        del self.frameListener
        del self.root
        del self.renderWindow

    
    def _createFrameListener(self):
        self.frameListener = CEGUIFrameListener(self.renderWindow, self.camera)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(False)

    def _createScene ( self ):

        self.GUIRenderer = CEGUI.OgreCEGUIRenderer( self.renderWindow, 
                Ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager )
        self.GUIsystem = CEGUI.System( self.GUIRenderer )




        ## load up CEGUI stuff... This is where we init the CEGUI window
        CEGUI.Logger.getSingleton().setLoggingLevel( CEGUI.Informative )
        CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme")
        self.GUIsystem.setDefaultMouseCursor("TaharezLook", "MouseArrow")
        self.GUIsystem.setDefaultFont( "BlueHighway-12")



        
        winMgr = CEGUI.WindowManager.getSingleton() 
        sheet = winMgr.createWindow( "DefaultWindow", "root_wnd" )

        mainMenuBackground = winMgr.createWindow("TaharezLook/FrameWindow", "Tesliz/MainMenuBackground")
        sheet.addChildWindow(mainMenuBackground)
        mainMenuBackground.setSize(CEGUI.UVector2(CEGUI.UDim(0.5, 0), CEGUI.UDim(0.5, 0)))
        mainMenuBackground.setXPosition(CEGUI.UDim(0.25, 0))
        mainMenuBackground.setYPosition(CEGUI.UDim(0.25, 0))
#        mainMenuBackground.setCloseButtonEnabled(false)
        mainMenuBackground.setText("Tesliz Menu Frame")


        startButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/StartButton")
        mainMenuBackground.addChildWindow(startButton)
        startButton.setText("Start Game")
        startButton.setXPosition(CEGUI.UDim(0.375, 0))
        startButton.setYPosition(CEGUI.UDim(0.3, 0))
        startButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        startButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleStart")
        startButton.setAlwaysOnTop(True)

#        jobButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/JobButton")
#        mainMenuBackground.addChildWindow(jobButton)
#        jobButton.setText("Jobs")
#        jobButton.setXPosition(CEGUI.UDim(0.375, 0))
#        jobButton.setYPosition(CEGUI.UDim(0.5, 0))
#        jobButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
#        jobButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleJobs")
#        jobButton.setAlwaysOnTop(True)

        quitButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/QuitButton")
        mainMenuBackground.addChildWindow(quitButton)
        quitButton.setText("Quit")
        quitButton.setXPosition(CEGUI.UDim(0.375, 0))
        quitButton.setYPosition(CEGUI.UDim(0.7, 0))
#        quitButton.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
        quitButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        quitButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuit")
        quitButton.setAlwaysOnTop(True)

        listBox = winMgr.createWindow("TaharezLook/Listbox", "Tesliz/MainMenuBackground/Listbox")
        mainMenuBackground.addChildWindow(listBox)


        CEGUI.System.getSingleton().setGUISheet( sheet )

    def handleQuit(self, e):
        self.frameListener.quit(e)
#        sf.FrameListener.requestShutdown()
        return True

    def handleStart(self, e):
        return

    
if __name__ == '__main__':
    try:
        application = MainMenuGUI()
        application.go()

    except Ogre.OgreException, e:
        print e