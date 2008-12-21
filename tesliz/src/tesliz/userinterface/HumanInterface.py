import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *
from userinterface.HumanInterface import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import data.util
import ogre.physics.OgreNewt as OgreNewt
import tactics.Unit
import util
class ShowSelected():
    def __init__(self,toexecute):
        self.toexecute = toexecute
        
        self.time = 0
        self.lastlist = []

    def cleanup(self):
        
        for last in self.lastlist:
            last.node.getAttachedObject(0).setMaterialName(last.job.material)
        self.lastlist = []
        if self.currentPosShow:
            if s.app.sceneManager.hasSceneNode(self.currentPosShow):
                s.app.sceneManager.destroySceneNode(self.currentPosShow)
    def execute(self,timer):
     
            
#        if self.time > 0:
#            self.time -= timer
#            return True
#        self.time = .5
                                                     
        name,position =data.util.fromCameraToMesh()
        curlist = []
        if name:
            if data.util.withinRange(self.toexecute.unit1.node.getPosition(),position,self.toexecute.range):
            
                for pos in self.toexecute.offset:
                    x,y,z = pos
                    x = x + position.x            
                    y = y + position.y
                    z = z + position.z
                    vec = Ogre.Vector3(x,y,z)
                    if self.toexecute.unittargeting:
                        obj = data.util.getValidUnit(vec)
                        if isinstance(obj, tactics.Unit.Unit):
                            obj.node.getAttachedObject(0).setMaterialName( "Spark/SOLID")
                            self.lastlist.append(obj)
                    else:
                        
                        vec = data.util.cleanup(data.util.getValidPos(vec))
                        if vec:
                            vec.y += 2
                            self.currentPosShow= data.util.show(vec,"RedMage/SOLID",self.currentPosShow)
                        
                    
                        
    
                
                #if obj:
                #    data.util.show(vec)
        
        if name == "terrain" or name != self.lastname:
            self.cleanup()
        self.lastname = name
        return True
    currentPosShow = None
    lastname = None
class HumanInterface:
    def __init__(self,player):
        self.player = player
        self.actionSelected = False
        self.removeFrom = None
        self.showSelected = None
        self.toremove = None
    
    lastClick = None
    cunit = None
    iexecute = None


    def displayActions(self):
        
        
        
        name = "actionlist"
        
        list = util.getNewWindow(name, util.listbox, "root_wnd", .735,.5, .1, .3,name)
      
        #list.setAlwaysOnTop(True)
        
        self.listmap = dict()

        
#        self.additem(list,"Move")
#        self.additem(list,"Attack")

        for trait in self.cunit.traits.getUsable():
            if trait:
                self.additem(list,trait.name)
        self.additem(list,"EndTurn")            
        list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAction")
        
#        if self.cunit.mental:
#            list = self.getNewWindow( "mentallist")
#            sheet.addChildWindow(list)
#            list.setText("list")
#            list.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( .4)))
#            list.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                
#            #list.setAlwaysOnTop(True)
#            #display mental
#            
#            for x in self.cunit.mental.getMentalCommands():
#                self.additem(list,x.name) 
#            list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleMental")   
    listholder = []
        

    def clickEntity(self,name,position,id,evt):
        #position.x = int(position.x)
        #position.y = int(position.y)
        #position.z = int(position.z)
        if not s.turnbased and s.unitmap.has_key(name) and not s.framelistener.pauseturns:
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
            
            self.choiceEnd()
            sf.Application.debugText = "Action Succeeded"
            if self.removeFrom:
                self.removeFrom.removeItem(self.toRemove)
                
                
            wind = CEGUI.WindowManager.getSingleton().getWindow("actionlist")
            isaction = True
            #the logic is kinda complicated
            #dir(self.currentTrait)
            if hasattr(self.abilityused,"action") and not self.abilityused.action:
                isaction = False
            toremovelist = []
            for x in range(0,wind.getItemCount()):
                item = wind.getListboxItemFromIndex(x)
                key = str(item.getText())
                if not self.cunit.traits[key]:
                    continue
                trait =self.cunit.traits[key]
                cisaction = True
                if hasattr(trait,"action") and not trait.action:
                    cisaction = False

                if isaction and cisaction:
                    toremovelist.append(item) 
            for x in toremovelist:
                wind.removeItem(x)
            self.cunit.traits[self.currentTrait].useAbility(self.abilityused)    
            self.actionSelected = False
            s.framelistener.unitqueue.addToQueue(self.cunit,self.iexecute)
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
            if CEGUI.WindowManager.getSingleton().isWindowPresent("abilitylist"):
                CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")
            #if hasattr(self.iexecute, "choiceEnd"):
            
            self.choiceEnd()
              
            item.setText(self.choosing)
            self.iexecute = None
            self.actionSelected = False
            return                    
        if self.actionSelected:
            return
        
        if not isinstance(e.window,CEGUI.ListboxTextItem):    
            self.choosing = item.getText()
            self.toRemove = item
#            if s.turnbased:
            self.removeFrom = e.window
            item.setText("Cancel")
#            else:
#                self.removeFrom = None
            
            self.actionSelected = item 
           
        if text == "EndTurn" or e.window.getItemCount() == 0:
            self.listmap = dict()
            self.endTurn()            
            return        
        self.currentTrait = text
        self.abilmap =self.cunit.traits[text].getAbilities()
        self.cunit.player.items
        list = self.abilmap.keys()
        print self.cunit
        if len(list) ==1:
            self.handleAbility(list[0])
            return
        name = "abilitylist"
        list1 = util.getNewWindow(name, util.listbox, "root_wnd", .835,.5, .1, .3,name)
                
        #list1.setAlwaysOnTop(True)
        
        self.listmap = dict()

        
        for ability in list:
            self.additem(list1,ability)
        list1.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAbility")
        
    currentTrait = None    
    def handleAbility(self, e):
        text = None
        if isinstance(e,str):
            text = e
        else:    
            text = e.window.getFirstSelectedItem().getText()
            item = e.window.getFirstSelectedItem()
        toexecute = self.abilmap[text]
        
        self.abilityused = self.abilmap[text]
        
        setStart(toexecute,self.cunit)
        self.choiceStart(toexecute.unit1.node.getPosition(), toexecute.range)
        self.showSelected = ShowSelected(toexecute)
        s.framelistener.unitqueue.addToQueue(self,self.showSelected)
        if toexecute.needsasecondclick:
            self.iexecute = copy.copy(toexecute)
        else:
            self.actionSelected.setText(self.choosing)
            self.cunit.traits[self.currentTrait].useAbility(self.abilityused)    
            self.actionSelected = False
            s.framelistener.unitqueue.addToQueue(self.cunit,copy.copy(toexecute))

        CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")
            
        
            
            #import time
            #time.sleep(1)
        return True

    def endTurn(self):
        CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        #CEGUI.WindowManager.getSingleton().destroyWindow("mentallist")
        self.actionSelected = False
        if self.cunit:
            self.cunit.player.endTurn()
            
    def choiceStart(self,pos,range):
        #create a mark that creates a small block
        self.toremove =data.util.markValid(pos, range, data.util.show)
        
    def choiceEnd(self):
        s.framelistener.unitqueue.clearActions(self)
        if self.showSelected:
            self.showSelected.cleanup()
        
        if self.toremove:
            for x in self.toremove:
                    
                s.app.sceneManager.getRootSceneNode().removeChild(x)
        self.toremove = None
    def endGame(self):
        s.cegui.destroy("actionlist")
        s.cegui.destroy("abilitylist")