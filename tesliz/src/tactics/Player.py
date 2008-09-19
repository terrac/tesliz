import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *

import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
s = Singleton()
class HumanPlayer(object):

    def __init__(self):
        self.actionSelected = False
        
    def endTurn(self):
        CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        s.turn.pause = False
        s.turn.nextUnitTurn()
        self.actionSelected = False

        
    def setVisualMarker(self,unit):
        pos = unit.body.getOgreNode().getPosition()
        sceneManager = s.app.sceneManager        
        #self.startPos =position  
        #self.endPos.y = position.y
        name = s.app.getUniqueName()
        mesh = "ellipsoid.mesh"
    
        scene_node = unit.node.createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        attachMe.setNormaliseNormals(True)
    
        scene_node.position = Ogre.Vector3(0,2,0)
        scene_node.getAttachedObject(0).setMaterialName("LightGreen/SOLID")
                
        size = .3
        scene_node.scale = Ogre.Vector3(size,size,size)
        
    
    #Tells you what the id of the last cegui hooks for the framelistener was    
    hookid = "Player1"
    
    unitlist = []
    lastClick = None
    cunit = None
    iexecute = None
    def startTurn(self,unit):
       self.cunit = unit 
       sf.Application.debugText = self.cunit.type
       #self.s.framelistener.cunit = cunit
       if s.turnbased:
           self.displayActions()
       
           
    
    caction = None
    def action(self,name):    
        caction = name       
        #add hooks if hookid is different from last
     #   if click.hookid != hookid:
     #       setupInput()
    def displayActions(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        list = winMgr.createWindow("TaharezLook/Listbox", "actionlist")
        sheet.addChildWindow(list)
        list.setText("actionlist")
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
    listholder = []
    
    

    

    def clickEntity(self,name,position):
        if not s.turnbased and s.unitmap.has_key(name):
            if s.unitmap[name] in self.unitlist:
                self.displayActions()
        if self.iexecute:
            unit = None
            if s.unitmap.has_key(name):
                unit = s.unitmap[name]           
            if not setStart(self.iexecute,None,unit,position):
                sf.Application.debugText = "Action failed"
                return
            sf.Application.debugText = "Action Succeeded"
            self.removeFrom.removeItem(self.toRemove)
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
        
        if text == "Cancel":
            try:
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
            self.removeFrom = e.window
            item.setText("Cancel")
            self.actionSelected = True 
           
        if text == "EndTurn" or e.window.getItemCount() == 0:
            self.listmap = dict()
            self.endTurn()            
            return        
        self.currentTrait = text
        list = self.cunit.traits[text].getAbilities()
        if len(list) ==1:
            self.handleAbility(list[0])
            return
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        list1 = winMgr.createWindow("TaharezLook/Listbox", "abilitylist")
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
        
        toexecute = self.cunit.traits[self.currentTrait].useAbility(text)
        try:
            setStart(toexecute,self.cunit)
            self.iexecute = copy.copy(toexecute)
        except Exception, ex:
            print repr(ex)
        CEGUI.WindowManager.getSingleton().destroyWindow("abilitylist")
            
        
            
            #import time
            #time.sleep(1)
        return True
            
  #  def endTurn(self):  
  #      s.turn.endTurn()
                
        
        
             
   # def setupInput(self):
   #     click.resetHooks()        
   #     click.hookid = hookid
        

       # if unitlist.contains(lastClick) and not s.unitmap.contains(name):
       #     move = Move(s.unitmap.get(lastClick),position)
       #     s.actionlist.append(move)
            #display unit data
            
        #lastClick = name
        
class ComputerPlayer(object):
    
    def __init__(self):    
        self.unitlist = []

    def getHookid(self):
        return self.__hookid


    def setHookid(self, value):
        self.__hookid = value


    def delHookid(self):
        del self.__hookid

    s = Singleton()
    hookid = "Computer1"
    def startTurn(self,unit):        
        lodis = 99
        lounit = None
        for eunit in s.unitmap.values():
            if not eunit.player ==self:
                dis = distance(eunit.node.getPosition(),unit.node.getPosition())
                if dis < lodis:
                    lodis =dis
                    lounit = eunit
        eunit = lounit
        sf.Application.debugText = str(unit) +"going after"+str(eunit)
        move = Move()
        newdir = eunit.node.getPosition() - unit.node.getPosition()
        newdir.normalise()
        newpos =eunit.node.getPosition()+ newdir * unit.getWantedRange()
        #print unit.getWantedRange()
        #print newpos
        #print eunit.node.getPosition()
        setStart(move,unit,None,newpos)
        s.framelistener.addToQueue(unit,move)
        map = dict()
        try:            
            while not self.getHighest(map,unit,eunit).action:
                print map
        except Exception,e:
            print e
        s.turn.pause = False    
        
        s.turn.nextUnitTurn()
        
        #go through playremap and find closest enemy.  Set to attack
       # a = 5       
    def clickEntity(self,name,position):
        if len(self.unitlist) > 0:
            return
        self.endGame()
    def endTurn(self):
        
        #CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        s.turn.nextUnitTurn()           

    def getHighest(self,map,unit,eunit):
        highest = 0
        hiabil = None
        for trait in unit.traits.keys():
            for abil in unit.traits[trait].listclasses:
                if highest <abil.value and not map.has_key(abil):
                    highest = abil.value
                    hiabil = abil
        map[hiabil] = True            
        hiabil = copy.copy(hiabil)            
        setStart(hiabil,unit,eunit)
        s.framelistener.addToQueue(unit,hiabil)
        
        s.log(str(unit)+" "+str(hiabil))
        return hiabil



    