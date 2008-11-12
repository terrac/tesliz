
# 
#
#


import sys
sys.path.insert(0,'..')


import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
import utilities.SampleFramework

from utilities.CEGUI_framework import *
from utilities.CEGUIFrameListener import *
from tactics.Singleton import *

def createUVector2( x, y):
    return CEGUI.UVector2(CEGUI.UDim(x,0), CEGUI.UDim(y,0))
def cegui_reldim ( x ) :
    return CEGUI.UDim((x),0)

def getJobsDict():
    SCHEME_JOBS = {}
    SCHEME_JOBS['Squire'] = "Squire"
    SCHEME_JOBS['Chemist'] = "Chemist"
    SCHEME_JOBS['Supreme_commander'] = "Supreme commander"

    return SCHEME_JOBS

s = Singleton()

class GEUIApplication(SampleFramework.Application):

    def __init__(self):
        SampleFramework.Application.__init__(self)
        self.CEGUIRenderer = 0
        self.CEGUISystem = 0
        self.MenuMode = True
        self.ListItems = []

    def _createScene(self):

        sceneManager = self.sceneManager
        sceneManager.ambientLight = ogre.ColourValue(0.25, 0.25, 0.25)

        # initiaslise CEGUI Renderer
        self.CEGUIRenderer = CEGUI.OgreCEGUIRenderer(self.renderWindow,
                ogre.RenderQueueGroupID.RENDER_QUEUE_OVERLAY,
                False, 3000,
                self.sceneManager)

        self.CEGUISystem = CEGUI.System(self.CEGUIRenderer)
        CEGUI.Logger.getSingleton().loggingLevel = CEGUI.Insane

        winMgr = CEGUI.WindowManager.getSingleton()

        # load scheme and set up defaults
        CEGUI.SchemeManager.getSingleton().loadScheme ("TaharezLookSkin.scheme")
        CEGUI.System.getSingleton().setDefaultMouseCursor ("TaharezLook", "MouseArrow")

        # load an image to use as a background
#        CEGUI.ImagesetManager.getSingleton().createImagesetFromImageFile("BackgroundImage", "GPN-2000-001437.tga")

        # here we will use a StaticImage as the root, then we 
        # can use it to place a background image
        background = winMgr.createWindow ("TaharezLook/StaticImage")
        # set area rectangle
        background.setArea (CEGUI.URect(cegui_reldim (0), cegui_reldim (0),
                                          cegui_reldim (1), cegui_reldim (1)))
        # disable frame and standard background
        background.setProperty ("FrameEnabled", "false")
        background.setProperty ("BackgroundEnabled", "false")
        # set the background image
        background.setProperty ("Image", "set:BackgroundImage image:full_image")
        # install this as the root GUI sheet
        CEGUI.System.getSingleton().setGUISheet (background)

        #/ set tooltip styles (by default there is none)
        CEGUI.System.getSingleton().setDefaultTooltip ("TaharezLook/Tooltip")

        # load some demo windows and attach to the background 'root'
        background.addChildWindow (winMgr.loadWindowLayout ("Jobs.layout", False))

        # Add party list to the partybox
        lbox = winMgr.getWindow ("FontDemo/PartyList")
        partyDict = s.unitmap
        for l in partyDict.keys():
            item = CEGUI.ListboxTextItem(l)
            item.setSelectionBrushImage("TaharezLook", "MultiListSelectionBrush")
            # ensure Python is in control of it's "deletion"
            item.AutoDeleted = False
            lbox.addItem( item)
            self.ListItems.append(item)

        # Add language list to the listbox
        lbox = winMgr.getWindow ("FontDemo/JobsList")
        jobsDict = getJobsDict()
        for l in jobsDict.keys():
            item = CEGUI.ListboxTextItem(l)
            item.setSelectionBrushImage("TaharezLook", "MultiListSelectionBrush")
            # ensure Python is in control of it's "deletion"
            item.AutoDeleted = False
            lbox.addItem( item)
            self.ListItems.append(item)

        # set up the language listbox callback
        lbox.subscribeEvent(
                    CEGUI.Listbox.EventSelectionChanged, self, "handleJobsSelection")
        # select the first language
        lbox.setItemSelectState(0, True)



    ## Event Handlers ##
    def setFontDesc(self):
        winMgr = CEGUI.WindowManager.getSingleton()
        mle = winMgr.getWindow("FontDemo/FontSample")
        f = mle.getFont()
        s = f.getProperty("Name")
        if f.isPropertyPresent("PointSize"):
            s += "." + f.getProperty("PointSize")
        winMgr.getWindow("FontDemo/FontDesc").setText(s)

    def handleJobsSelection(self, e):
        lbox = e.window
        if lbox.getFirstSelectedItem():
            idx = lbox.getItemIndex(lbox.getFirstSelectedItem())
            winMgr = CEGUI.WindowManager.getSingleton()

            cs = CEGUI.String()
            cs.assign( getJobsDict().values()[idx].encode("utf-8") )
            winMgr.getWindow("FontDemo/FontSample").setText(cs)

        return True


#    def _createCamera(self):
#        self.camera = self.sceneManager.createCamera("PlayerCam")
#        self.camera.nearClipDistance = 5

    def _createFrameListener(self):
        self.frameListener = CEGUIFrameListener(self.renderWindow, self.camera)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)

    def __del__(self):
        "Clear variables, this is needed to ensure the correct order of deletion"
        del self.camera
        del self.sceneManager
        del self.frameListener
        del self.CEGUISystem
        del self.CEGUIRenderer
        del self.root
        del self.renderWindow        


if __name__ == '__main__':
    try:
        ta = GEUIApplication()
        ta.go()
    except ogre.OgreException, e:
        print e
