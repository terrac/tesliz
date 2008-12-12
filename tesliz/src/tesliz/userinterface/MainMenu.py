
from tactics.Singleton import *
from data.jobs import *
from tactics.Unit import Unit
import ogre.gui.CEGUI as CEGUI
import util
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.renderer.OGRE as Ogre
s = Singleton()



class JobsMenu:
    def setup(self,unit):
        if not unit:
            return
        
        list1 = util.getNewWindow("joblist","Main/Window")
                
        list1.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.5)))
        list1.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                

        self.unit = unit
        for job in unit.joblist:
            util.addItem(self,list1,job.getName())
        list1.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleJobsSelection")
    def handleJobsSelection(self, e):
        lbox = e.window
        if lbox.getFirstSelectedItem():
            jobName = lbox.getFirstSelectedItem()
            jobNameText = jobName.getText()
            idx = lbox.getItemIndex(jobName)
            s.log("handleJobSelection: jobName = "+str( jobNameText),self)

            
            if self.unit != None and self.unit.job.getName() != jobNameText:
                for x in self.unit.joblist:
                    if x.getName() == jobNameText:
                        changeTo(self.unit, x)
                    
            #cs = CEGUI.String()
            #cs.assign( self.getJobsDict().values()[idx].encode("utf-8") )
            #winMgr = CEGUI.WindowManager.getSingleton()
            #winMgr.getWindow("Main/FontSample").setText(cs)

        return True
class ItemsMenu:
    def setup(self,unit):
        pass
class AbilitiesMenu:
    def setup(self,unit):
        pass

class MainMenu:
    
    def __init__(self, renderWindow, sceneManager):
        self.ListItems = []
        if s.initCEGUI != True:
            self.initCEGUIStuff(renderWindow, sceneManager)
            s.initCEGUI = True
        self.editmap ={"Items":ItemsMenu(),"Jobs":JobsMenu(),"Abilities":AbilitiesMenu()}
        self.unit = None


    def initCEGUIStuff(self, renderWindow, sceneManager):
        self.GUIRenderer = CEGUI.OgreCEGUIRenderer( renderWindow, 
                Ogre.RENDER_QUEUE_OVERLAY, False, 3000, sceneManager )
        self.GUIsystem = CEGUI.System( self.GUIRenderer )
        ## load up CEGUI stuff...
        CEGUI.Logger.getSingleton().setLoggingLevel( CEGUI.Informative )
#         CEGUI.SchemeManager.getSingleton().loadScheme("WindowsLook.scheme") #../../Media/GUI/schemes/WindowsLook.scheme")
#         self.GUIsystem.setDefaultMouseCursor("WindowsLook", "MouseArrow")
#         self.GUIsystem.setDefaultFont("Commonwealth-10")
        CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme") 
        self.GUIsystem.setDefaultMouseCursor("TaharezLook",  "MouseArrow") 
        self.GUIsystem.setDefaultFont( "BlueHighway-12")
        
        sheet = CEGUI.WindowManager.getSingleton().createWindow( "DefaultWindow", "root_wnd" )
        CEGUI.System.getSingleton().setGUISheet( sheet )
        CEGUI.System.getSingleton().getRenderer().setTargetRenderQueue(Ogre.RENDER_QUEUE_OVERLAY, True);
         

    def setupStartMenu(self):
 #       sheet = CEGUI.System.getSingleton().getGUISheet()
        winMgr = CEGUI.WindowManager.getSingleton()
        
        mainMenuBackground = util.getNewWindow( "Tesliz/MainMenuBackground", "root_wnd", "TaharezLook/FrameWindow")
#        sheet.addChildWindow(mainMenuBackground)
        mainMenuBackground.setSize(CEGUI.UVector2(CEGUI.UDim(0.25, 0), CEGUI.UDim(0.25, 0)))
        mainMenuBackground.setXPosition(CEGUI.UDim(0, 0))
        mainMenuBackground.setYPosition(CEGUI.UDim(0, 0))
#        mainMenuBackground.setCloseButtonEnabled(false)
        mainMenuBackground.setText("Tesliz Menu Frame")



        jobButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/JobButton")
        mainMenuBackground.addChildWindow(jobButton)
        jobButton.setText("Edit Units")
        jobButton.setXPosition(CEGUI.UDim(0.375, 0))
        jobButton.setYPosition(CEGUI.UDim(0.5, 0))
        jobButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        jobButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleEditMenuCreation")
        #jobButton.setAlwaysOnTop(True)

        quitButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/QuitButton")
        mainMenuBackground.addChildWindow(quitButton)
        quitButton.setText("Quit")
        quitButton.setXPosition(CEGUI.UDim(0.375, 0))
        quitButton.setYPosition(CEGUI.UDim(0.7, 0))
#        quitButton.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
        quitButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        quitButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuitGameFromMenu")
        #quitButton.setAlwaysOnTop(True)
        


    def createEditMenu(self):
        sheet = CEGUI.System.getSingleton().getGUISheet()
        winMgr = CEGUI.WindowManager.getSingleton()
        

        #/ set tooltip styles (by default there is none)
        CEGUI.System.getSingleton().setDefaultTooltip ("TaharezLook/Tooltip")

        # load some demo windows and attach to the background 'root'
        sheet.addChildWindow (winMgr.loadWindowLayout ("edit.layout", False))
        
        # REFACTOR - Set up the callbacks for the buttons loaded by the layout
        backButton = sheet.getChild("cmdBackToMenu")
        backButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleDeleteEditCreateStartMenu")
        
        # Add party list to the partybox
        lbox = winMgr.getWindow ("Main/PartyList")
        
        
       
        for l in s.cplayer.unitlist:
            
            util.addItem(self,lbox,l.name)

        # set up the language listbox callback
        lbox.subscribeEvent(
                    CEGUI.Listbox.EventSelectionChanged, self, "handlePartySelection")
        if len(s.cplayer.unitlist) > 0:
            item = lbox.getListboxItemFromIndex(0)
            item.setSelected(True)
            self.unit = s.unitmap[str(item.getText())]
        lbox = winMgr.getWindow ("Main/EditList")
        
        
      
        for l in self.editmap.keys():
            util.addItem(self,lbox,l)

        # set up the language listbox callback
        lbox.subscribeEvent(
                    CEGUI.Listbox.EventSelectionChanged, self, "handleEditSelection")



 
        
    def handleQuitGameFromMenu(self, e):
        s.app.handleQuit(e)
        
    
    
    def handleDeleteEditCreateStartMenu(self, e):

        util.destroyWindow("editmenu")
        self.setupStartMenu()
        
    def handleEditMenuCreation(self, e):
        util.destroyWindow("Tesliz/MainMenuBackground")
        self.createEditMenu()
        
    # Global variable for the time being, the currently selected unit object

    def handlePartySelection(self, e):
        # Need to find the unit object based off the string name of the unit
        lbox = e.window
        if lbox.getFirstSelectedItem():
            unitName = str(lbox.getFirstSelectedItem().getText())
            s.log("Selected Party Member: "+ unitName,self)

            self.unit = s.unitmap[unitName]
            

        return True

    def handleEditSelection(self, e):
        # Need to find the unit object based off the string name of the unit
        lbox = e.window
        if lbox.getFirstSelectedItem():
            etext = str(lbox.getFirstSelectedItem().getText())
            
            self.editmap[etext].setup(self.unit)

            
            

        return True
  