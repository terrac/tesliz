import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *
from userinterface.HumanInterface import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf

class HumanInterface:
    def __init__(self,player):
        self.player = player
        self.actionSelected = False
        self.removeFrom = None

    
    lastClick = None
    cunit = None
    iexecute = None
    def getNewWindow(self, name):
        winMgr = CEGUI.WindowManager.getSingleton()
        if winMgr.isWindowPresent(name):
            CEGUI.WindowManager.getSingleton().destroyWindow(name)
        #    list = winMgr.getWindow(name)
        #    list.resetList()
        #else:
        
        list = winMgr.createWindow("TaharezLook/Listbox", name)
        return list

    def displayActions(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        
        
        name = "actionlist"
        winMgr = CEGUI.WindowManager.getSingleton()
        list = self.getNewWindow(name)
        sheet.addChildWindow(list)
        list.setText(name)
        list.setPosition(CEGUI.UVector2(cegui_reldim(0.735), cegui_reldim( 0.5)))
        list.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                
        list.setAlwaysOnTop(True)
        
        self.listmap = dict()

        
#        self.additem(list,"Move")
#        self.additem(list,"Attack")

        for trait in self.cunit.traits:
            self.additem(list,trait)
        self.additem(list,"EndTurn")            
        list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAction")
        
        if self.cunit.mental:
            list = self.getNewWindow( "mentallist")
            sheet.addChildWindow(list)
            list.setText("list")
            list.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( .4)))
            list.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                
            list.setAlwaysOnTop(True)
            #display mental
            
            for x in self.cunit.mental.getMentalCommands():
                self.additem(list,x.name) 
            list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleMental")   
    listholder = []
    
    def handleMental(self, e):
        #aoeu dir(e.window.getFirstSelectedItem().getText())
        text = None
        if isinstance(e,str):
            text = e
        else:
            try:    
                text = e.window.getFirstSelectedItem().getText()
            except:
                return
        
        for x in  self.cunit.mental.getMentalCommands():
            if x.name == text:
                toexecute = x
        #try:
        toexecute.clicked()
        #except:
        #    pass
        try:
            setStart(toexecute,self.cunit)
            if toexecute.needsasecondclick:
                self.iexecute = copy.copy(toexecute)
            
        except Exception, ex:
            print repr(ex)
        s.log(text)
        self.removeFrom = None
        #CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")    

    

    def clickEntity(self,name,position):
        if not s.turnbased and s.unitmap.has_key(name):
            if s.unitmap[name] in self.player.unitlist:
            
                self.cunit = s.unitmap[name] 
                #s.unitmap[name].startTurn() 
                self.displayActions()
        if self.iexecute:
            unit = None
            if s.unitmap.has_key(name):
                unit = s.unitmap[name]  
                     
            if not setStart(self.iexecute,None,unit,position):
                sf.Application.debugText = "Action failed"
                s.playsound()
                return
            sf.Application.debugText = "Action Succeeded"
            if self.removeFrom:
                self.removeFrom.removeItem(self.toRemove)
            self.cunit.traits[self.currentTrait].useAbility(self.abilityused)    
            self.actionSelected = False
            s.framelistener.addToQueue(self.cunit,self.iexecute)
            self.iexecute = None    
    def additem(self,list,name):        
        item =CEGUI.ListboxTextItem (name)        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        list.addItem(item)
        
    def handleAction(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        item =e.window.getFirstSelectedItem()
        print text
        if text == "Cancel":
            try:
                CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")
                self.iexecute.choiceEnd()
            except:
                pass  
            item.setText(self.choosing)
            self.iexecute = None
            self.actionSelected = False
            return                    
        if self.actionSelected:
            return
        
        if not isinstance(e.window,CEGUI.ListboxTextItem):    
            self.choosing = item.getText()
            self.toRemove = item
            if s.turnbased:
                self.removeFrom = e.window
                item.setText("Cancel")
            else:
                self.removeFrom = None
            
            self.actionSelected = item 
           
        if text == "EndTurn" or e.window.getItemCount() == 0:
            self.listmap = dict()
            self.endTurn()            
            return        
        self.currentTrait = text
        list = self.cunit.traits[text].getAbilities()
        print self.cunit
        if len(list) ==1:
            self.handleAbility(list[0])
            return
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        list1 = self.getNewWindow("abilitylist")
        sheet.addChildWindow(list1)
        list1.setText("abilitylist")
        list1.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.5)))
        list1.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                
        list1.setAlwaysOnTop(True)
        
        self.listmap = dict()

        
        for ability in list:
            self.additem(list1,ability)
        list1.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAbility")
        
    currentTrait = None    
    def handleAbility(self, e):
        #aoeu dir(e.window.getFirstSelectedItem().getText())
        text = None
        if isinstance(e,str):
            text = e
        else:    
            text = e.window.getFirstSelectedItem().getText()
            item = e.window.getFirstSelectedItem()
        toexecute = self.cunit.traits[self.currentTrait].getAbility(text)
        self.abilityused = text
        try:
            setStart(toexecute,self.cunit)
            if toexecute.needsasecondclick:
                self.iexecute = copy.copy(toexecute)
            else:
                self.actionSelected.setText(self.choosing)
                self.cunit.traits[self.currentTrait].useAbility(self.abilityused)    
                self.actionSelected = False
                s.framelistener.addToQueue(self.cunit,copy.copy(toexecute))
        except Exception, ex:
            print repr(ex)
        CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")
            
        
            
            #import time
            #time.sleep(1)
        return True

    def endTurn(self):
        CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        CEGUI.WindowManager.getSingleton().destroyWindow("mentallist")
        self.actionSelected = False
        if self.cunit:
            self.cunit.player.endTurn()