
from tactics.Singleton import *
from data.jobs import *
from tactics.Unit import Unit
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf

s = Singleton()

class CEGUI_Menus:
    
    def __init__(self, renderWindow, sceneManager):
        self.ListItems = []
        if s.initCEGUI != True:
            self.initCEGUIStuff(renderWindow, sceneManager)
            s.initCEGUI = True


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

    def startMenu(self):
        sheet = CEGUI.System.getSingleton().getGUISheet()
        winMgr = CEGUI.WindowManager.getSingleton()
        mainMenuBackground = winMgr.createWindow("TaharezLook/FrameWindow", "Tesliz/MainMenuBackground")
        sheet.addChildWindow(mainMenuBackground)
        mainMenuBackground.setSize(CEGUI.UVector2(CEGUI.UDim(0.25, 0), CEGUI.UDim(0.25, 0)))
        mainMenuBackground.setXPosition(CEGUI.UDim(0, 0))
        mainMenuBackground.setYPosition(CEGUI.UDim(0, 0))
#        mainMenuBackground.setCloseButtonEnabled(false)
        mainMenuBackground.setText("Tesliz Menu Frame")


        startButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/StartButton")
        mainMenuBackground.addChildWindow(startButton)
        startButton.setText("Start Game")
        startButton.setXPosition(CEGUI.UDim(0.375, 0))
        startButton.setYPosition(CEGUI.UDim(0.3, 0))
        startButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        startButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleStartGameFromMenu")
        startButton.setAlwaysOnTop(True)

        jobButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/JobButton")
        mainMenuBackground.addChildWindow(jobButton)
        jobButton.setText("Jobs")
        jobButton.setXPosition(CEGUI.UDim(0.375, 0))
        jobButton.setYPosition(CEGUI.UDim(0.5, 0))
        jobButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        jobButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleJobMenuCreation")
        jobButton.setAlwaysOnTop(True)

        quitButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/QuitButton")
        mainMenuBackground.addChildWindow(quitButton)
        quitButton.setText("Quit")
        quitButton.setXPosition(CEGUI.UDim(0.375, 0))
        quitButton.setYPosition(CEGUI.UDim(0.7, 0))
#        quitButton.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
        quitButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        quitButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuitGameFromMenu")
        quitButton.setAlwaysOnTop(True)
        
    def deleteStartMenu(self):
        winMgr = CEGUI.WindowManager.getSingleton()
        winMgr.destroyWindow("Tesliz/MainMenuBackground")

    def createJobMenu(self):
        sheet = CEGUI.System.getSingleton().getGUISheet()
        winMgr = CEGUI.WindowManager.getSingleton()
        
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
        sheet.addChildWindow(background)

        #/ set tooltip styles (by default there is none)
        CEGUI.System.getSingleton().setDefaultTooltip ("TaharezLook/Tooltip")

        # load some demo windows and attach to the background 'root'
        background.addChildWindow (winMgr.loadWindowLayout ("Jobs.layout", False))
        
        # REFACTOR - Set up the callbacks for the buttons loaded by the layout
        backButton = background.getChild("cmdBackToMenu")
        backButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleDeleteJobCreateStartMenu")
        
        # Add party list to the partybox
        lbox = winMgr.getWindow ("FontDemo/PartyList")
        
        ################ TEMP ##################
        del s.cplayer.unitlist[:]
        firstTempUnit = Unit()
        firstTempUnit.name = "Shygar"
        squire = Squire()
        # This function needs to be less generic, it changes the jobs of the unit passed in
        changeTo(firstTempUnit,squire)
        s.cplayer.unitlist.append(firstTempUnit)
        
        secondTempUnit = Unit()
        secondTempUnit.name = "Korben"
        wizard = Wizard()
        # This function needs to be less generic, it changes the jobs of the unit passed in
        changeTo(secondTempUnit,wizard)
        s.cplayer.unitlist.append(secondTempUnit)
        ############### END TEMP ######################
        
        s.log("Current Player Unit List: ", s.cplayer.unitlist)
        partyDict = s.cplayer.unitlist
        for l in partyDict:
            item = CEGUI.ListboxTextItem(l.name)
            item.setSelectionBrushImage("TaharezLook", "MultiListSelectionBrush")
            # ensure Python is in control of it's "deletion"
            item.AutoDeleted = False
            lbox.addItem( item)
            self.ListItems.append(item)

        # set up the language listbox callback
        lbox.subscribeEvent(
                    CEGUI.Listbox.EventSelectionChanged, self, "handlePartySelection")

        
        # Add language list to the listbox
        lbox = winMgr.getWindow ("FontDemo/JobsList")
        jobsDict = self.getJobsDict()
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

    def deleteJobMenu(self):
        winMgr = CEGUI.WindowManager.getSingleton()
        winMgr.destroyWindow("root")
        # Not sure if i need to do this:
        winMgr.destroyWindow("FontDemo/PartyList")
        
    def handleStartGameFromMenu(self, e):
        # Remove the menu
        self.deleteStartMenu()
        self.loadScene("scene01")
        
    def handleQuitGameFromMenu(self, e):
        self.handleQuit(e)
        
    def getJobsDict(self):
        SCHEME_JOBS = {}
        SCHEME_JOBS['Squire'] = "Squire"
        SCHEME_JOBS['Chemist'] = "Chemist"
        SCHEME_JOBS['Wizard'] = "Wizard"
    
        return SCHEME_JOBS
    
    def handleDeleteJobCreateStartMenu(self, e):
        self.deleteJobMenu()
        self.startMenu()
        
    def handleJobMenuCreation(self, e):
        self.deleteStartMenu()
        self.createJobMenu()
        
    # Global variable for the time being, the currently selected unit object
    selectedUnit = None
    def handlePartySelection(self, e):
        # Need to find the unit object based off the string name of the unit
        lbox = e.window
        if lbox.getFirstSelectedItem():
            unitName = lbox.getFirstSelectedItem().getText()
            s.log("Selected Party Member: ", unitName)

            partyDict = s.cplayer.unitlist
            for l in partyDict:
                if l.name == unitName:
                    # Save the unit object that matches
                    self.selectedUnit = l
            
            if self.selectedUnit == None:
                return False
            
            jobName = self.selectedUnit.getJob().jobName()
            s.log("handlePartySelection: jobName = ", jobName)
            
            winMgr = CEGUI.WindowManager.getSingleton()

#            cs = CEGUI.String()
#            cs.assign( self.getJobsDict().values()[idx].encode("utf-8") )
            jobListBox = winMgr.getWindow("FontDemo/JobsList")
            listBoxItemFound = jobListBox.findItemWithText(jobName, None)
            # Set the already defined job in the job list for this selected unit, deselect the others
            jobListBox.clearAllSelections()
            jobListBox.setItemSelectState(listBoxItemFound, True)

        return True

    def handleJobsSelection(self, e):
        lbox = e.window
        if lbox.getFirstSelectedItem():
            jobName = lbox.getFirstSelectedItem()
            jobNameText = jobName.getText()
            idx = lbox.getItemIndex(jobName)
            s.log("handleJobSelection: jobName = ", jobNameText)

            # Make this its own function, prob in the jobs.py file
            if jobNameText == "Squire":
                if self.selectedUnit != None and self.selectedUnit.getJob().jobName() != jobNameText:
                    # As stated above, make this changeTo function a more defined name
                    # Also, we need to have a way to revert this change if users don't hit the save button
                    changeTo(self.selectedUnit, Squire())
            elif jobNameText == "Wizard":
                if self.selectedUnit != None and self.selectedUnit.getJob().jobName() != jobNameText:
                    # As stated above, make this changeTo function a more defined name
                    # Also, we need to have a way to revert this change if users don't hit the save button
                    changeTo(self.selectedUnit, Wizard())
            elif jobNameText == "Chemist":
                if self.selectedUnit != None and self.selectedUnit.getJob().jobName() != jobNameText:
                    # As stated above, make this changeTo function a more defined name
                    # Also, we need to have a way to revert this change if users don't hit the save button
                    changeTo(self.selectedUnit, Chemist())
                    
            cs = CEGUI.String()
            cs.assign( self.getJobsDict().values()[idx].encode("utf-8") )
            winMgr = CEGUI.WindowManager.getSingleton()
            winMgr.getWindow("FontDemo/FontSample").setText(cs)

        return True

        
