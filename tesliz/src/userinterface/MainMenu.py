from tactics.Singleton import *

from tactics.Unit import Unit
import ogre.gui.CEGUI as CEGUI
import util
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.renderer.OGRE as Ogre
import data.jobs
s = Singleton()
import data.jobs
import tactics.util
import data.items 
    

class JobsMenu:
    def setup(self,unit,pwindow):
        if not unit:
            return
        
        
        self.joblist =list1 =util.getNewWindow("joblist", util.listbox, pwindow, .6,.5,.1,.3)             
        self.jobname = util.getNewWindow("jobname", util.statictext, pwindow,.6, .4, .1, .1, unit.job.getName())
        self.unit = unit
        for job in unit.joblist:
            util.addItem(self,list1,job.getName())
        list1.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleJobsSelection")
    def teardown(self):
        self.joblist.setVisible(False)
        self.jobname.setVisible(False)
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
                        x.changeTo(self.unit)
            self.jobname.setText(self.unit.job.getName())
            #cs = CEGUI.String()
            #cs.assign( self.getJobsDict().values()[idx].encode("utf-8") )
            #winMgr = CEGUI.WindowManager.getSingleton()
            #winMgr.getWindow("Main/FontSample").setText(cs)
        s.mainmenu.updateDisplay()
        return True
class AbilityMenu:

    def setupAbil(self):
        for x in self.list:
            if self.map.has_key(x) and self.map[x]:
                x = self.map[x].getName()
            
            util.addItem(self, self.abilheld, x)
        
        self.abilheld.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "showTraits")




    
    list = ["Secondary","Reaction","Support","Movement"]

    def setupMenu(self, pwindow):
        util.getNewWindow("abilityjobname", util.statictext, pwindow, .5, .1, .2, .1, self.unit.job.getName())
        self.abilheld = util.getNewWindow("abilitiesheld", util.listbox, pwindow, .5, .2, .2, .3)

        
    def getMap(self,unit):        
        self.map = unit.traits.getMap()
    
    
        
    def setup(self,unit,pwindow):
        self.listtype = None
        self.pwindow = pwindow
        self.unit = unit
        self.getMap(unit)
        self.setupMenu(pwindow)
        self.setupAbil()
    def showTraits(self,e):
        if not e.window.getFirstSelectedItem():
            return
        self.itemselected = e.window.getFirstSelectedItem()
        self.typeindex = e.window.getItemIndex(e.window.getFirstSelectedItem())
        self.type =text = self.list[self.typeindex]
        
        self.setupList(text)    
        
    def setupList(self, type):
        self.listtype =util.getNewWindow("listtype", util.listbox, self.pwindow, .7,.2,.2,.3)    
        self.typelist = self.getList(type)
        for x in self.typelist:
            util.addItem(self, self.listtype, x.getName())
        
        self.listtype.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "setType")
    
    def getList(self,type):
        valid = []
        if type == "Secondary":
            for x in self.unit.joblist:
                if x != self.unit.job:
                    valid.append(x)
        else:    
            for x in self.unit.joblist:
                if data.jobs.choosablemap.has_key(type):
                    typemap = data.jobs.choosablemap[type]
                    if typemap.has_key(x.getName()):
                        x.getTraits(self.unit)
                        list =typemap[x.getName()]
                        for y in list:
                            if y.getName() in x.learnedabilitynames:
                                valid.append(y)
        return valid
    def setType(self,e):
        if not e.window.getFirstSelectedItem():
            return
        toadd = self.typelist[e.window.getItemIndex(e.window.getFirstSelectedItem())]
        #this should be the ability map on the unit trait so it could alse be self.unit.traits.map0self.type] = toadd
        if self.type == "Secondary":
            self.map[self.type] = toadd.getTraits(self.unit)
        else:
            self.map[self.type] = toadd
        #self.unit.traits.map[self.type] = toadd
        self.itemselected.setText(toadd.getName())
        tactics.util.resetAttributes(self.unit)
        self.listtype.setVisible(False)
        self.removeFromList(toadd)
        
        s.mainmenu.updateDisplay()
    def removeFromList(self,toadd):
        pass
    def teardown(self):
        self.abilheld.setVisible(False)
        if self.listtype:
            self.listtype.setVisible(False)
        pass
class ItemsMenu(AbilityMenu):
    list = ["head","body","weapon"]
    def setupMenu(self, pwindow):
        
        self.abilheld = util.getNewWindow("abilitiesheld", util.listbox, pwindow, .5, .2, .2, .3)
        self.removeitem = util.getNewWindow("removeitem", util.button, pwindow, .5, .5, .2, .1, "removeItem")
        self.removeitem.subscribeEvent(CEGUI.PushButton.EventClicked, self, "removeItem")
        self.typelist = []
    
    def removeFromList(self,toadd):
        self.unit.player.items.add(toadd.getName())
    def removeItem(self,e):
        if  not self.abilheld.getFirstSelectedItem():
            return
        item =self.abilheld.getFirstSelectedItem()
        text = str(item.getText())
        if text in self.list:
            return
        self.unit.player.items.add(text)
        type = self.list[self.abilheld.getItemIndex(self.abilheld.getFirstSelectedItem())]
        self.unit.items.remove(type)
        self.setupList(type)
        
        self.abilheld = util.getNewWindow("abilitiesheld", util.listbox, self.pwindow, .5, .2, .2, .3)
        self.abilheld.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "showTraits")
        self.setupAbil()
        self.listtype.setVisible(False)
    def getMap(self,unit):
        self.map = unit.items.getMap()
    def getList(self,type):
        valid = []
        itemmap =self.unit.player.items.getMap()
        for x in itemmap.keys():
            item =getattr(data.items, x)
            if item.type == type and len(item.allowed) == 0 or self.unit.job.getName() in item.allowed:
                valid.append(item())
        return valid
        
class LearnMenu:
    def setup(self,unit,pwindow):
        self.unit = unit
        
        self.abiltohold =util.getNewWindow("abilitiestohold", util.listbox, "Main/Window", .7,.1,.2,.4)
        #util.addItem(self, self.abiltohold,"Try" )
        util.addItem(self, self.abiltohold,"Learn" )
        self.abiltohold.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "doAbil")
        
    def doAbil(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        if text == "Learn":
            self.setupLearning()
            
    def setupLearning(self):
        self.learnwindow =util.getNewWindow("learnwindow", util.frame, util.rootwindow, .2,.2,.8,.8)
        self.joblist =util.getNewWindow("joblist", util.listbox, self.learnwindow, .2,.2,.3,.8)
        self.learnwindow.setAlwaysOnTop(True)
        for job in self.unit.joblist:
             util.addItem(self, self.joblist,job.getName())
        self.joblist.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "getAbilList")
    def getAbilList(self,e):
        if isinstance(e, str):
            text = e
        else: 
            if not e.window.getFirstSelectedItem():
                return
            text = str(e.window.getFirstSelectedItem().getText())
        self.jobselected = util.getNewWindow("jobselected", util.statictext,self.learnwindow, .5,.2,.2,.1)
        self.jobselected.setText(text)
        self.jobexp = util.getNewWindow("jobexp", util.statictext,self.learnwindow, .8,.2,.1,.1)
        
        self.abillist =util.getNewWindow("abillist", util.listbox, self.learnwindow, .2,.3,.5,.8)
        self.learnedlist =util.getNewWindow("learnedlist", util.listbox, self.learnwindow, .7,.3,.2,.8)
        #eventally create tabs for the reaction and so on abilities
        for x in self.unit.joblist:
            if x.getName() == text:
                learnednames= x.learnedabilitynames
                self.currentjob = x
                self.jobexp.setText(str(x.exp))
        for x in data.jobs.jobabilitymap[text].getClassList():
             util.addItem(self,self.abillist,x.name )
             learnedDisplay = "False" + str(x.jobpoints)
             if x.name in learnednames:
                 learnedDisplay = "True"
                 
                 
             util.addItem(self, self.learnedlist, learnedDisplay)
        self.abillist.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "learnAbility")
    
    def learnAbility(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        jobtype = str(self.jobselected.getText())
        for x in data.jobs.jobabilitymap[jobtype].getClassList():
            if text == x.name:
                self.currentability = x
        if self.currentjob.exp > self.currentability.jobpoints:
            self.currentjob.learnedabilitynames.append(text)
            self.currentjob.exp -= self.currentability.jobpoints
        self.getAbilList(jobtype)
        #self.unit.job.changeTo(self.unit)
    
    def teardown(self):
        
        self.abiltohold.setVisible(False)
        
class MainMenu:
    
    def __init__(self, renderWindow, sceneManager):
        self.ListItems = []
        if s.initCEGUI != True:
            self.initCEGUIStuff(renderWindow, sceneManager)
            s.initCEGUI = True
        self.editmap ={"Items":ItemsMenu(),"Jobs":JobsMenu(),"Abilities":AbilityMenu(),"Learn":LearnMenu()}
        self.unit = None
        self.prevedit = None
        s.mainmenu = self


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
        
        mainMenuBackground = util.getNewWindow( "Tesliz/MainMenuBackground",  "TaharezLook/FrameWindow","root_wnd")
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
        s.cegui.inputcaptured = True
#        pframe =util.getNewWindow("Main/Window", util.frame, "root_wnd", .1, .11, .8, .8, "MainMenu")
#        #util.getNewWindow("Main/StaticBack",util.multieditbox, pframe, .0, 0, 1, 1)
#        util.getNewWindow("Main/FontSample",util.multieditbox, pframe, .05, .11, .4, .4)
#        util.getNewWindow("Main/PartyList", util.listbox, pframe, .05, .55, .15, .30)
#        util.getNewWindow("Main/EditList", util.listbox, pframe, .25, .55, .15, .30)
#        util.getNewWindow("cmdBackToMenu", util.button, pframe, .3, .9, .1, .07,"back")
        #util.recursiveSet(sheet, util.setLayoutCallbacks)
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
            self.unit = s.cplayer.unitlist[0]
            self.updateDisplay()
        lbox = winMgr.getWindow ("Main/EditList")
        
        
      
        for l in self.editmap.keys():
            util.addItem(self,lbox,l)

        # set up the language listbox callback
        lbox.subscribeEvent(
                    CEGUI.Listbox.EventSelectionChanged, self, "handleEditSelection")



 
        
    def handleQuitGameFromMenu(self, e):
        s.app.handleQuit(e)
        
    
    
    def handleDeleteEditCreateStartMenu(self, e):
        s.cegui.inputcaptured = False
        util.destroyWindow("editmenu")
        self.setupStartMenu()
        
    def handleEditMenuCreation(self, e):
        if not s.cplayer.unitlist:
            return
        util.destroyWindow("Tesliz/MainMenuBackground")
        self.createEditMenu()
        
    # Global variable for the time being, the currently selected unit object

    def handlePartySelection(self, e):
        # Need to find the unit object based off the string name of the unit
        lbox = e.window
        if lbox.getFirstSelectedItem():
            unitName = str(lbox.getFirstSelectedItem().getText())
            s.log("Selected Party Member: "+ unitName,self)
            for unit in s.playermap["Player1"].unitlist:
                if unit.getName() == unitName:
                    self.unit = unit
            

        return True

    def handleEditSelection(self, e):
        # Need to find the unit object based off the string name of the unit
        lbox = e.window
        if lbox.getFirstSelectedItem():
            etext = str(lbox.getFirstSelectedItem().getText())
            if self.prevedit:
                self.prevedit.teardown()
            self.editmap[etext].setup(self.unit,"Main/Window")
            self.updateDisplay()
            self.prevedit = self.editmap[etext]
            
            

        return True
    def updateDisplay(self):
        text = "\n"+str(self.unit.attributes)
        s.cegui.getWindow("Main/Display").setText(str(self.unit)+text)
  