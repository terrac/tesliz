import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
#from data.traits.Generictraits import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
s = Singleton()
class HumanPlayer(object):

    #def __init__(self):
        
    def endTurn(self):
        CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        s.turn.nextUnitTurn()

        
    
    
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
            if unitlist.has_key(s.unitmap[name]):
                self.displayActions()
        if self.iexecute:
            unit = None
            if s.unitmap.has_key(name):
                unit = s.unitmap[name]           
            if not self.iexecute.setUnitAndPosition(unit,position):
                sf.Application.debugText = "Action failed"
                return
            sf.Application.debugText = "Action Succeeded"
            s.framelistener.runningexecutes.append(self.iexecute)
            self.iexecute = None    
    def additem(self,list,name):        
        item =CEGUI.ListboxTextItem (name)        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        list.addItem(item)
        
    def handleAction(self,e):
        text = str(e.window.getFirstSelectedItem().getText())
        
        if not isinstance(e.window,CEGUI.ListboxTextItem):    
            e.window.removeItem(e.window.getFirstSelectedItem())   
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
        list = winMgr.createWindow("TaharezLook/Listbox", "abilitylist")
        sheet.addChildWindow(list)
        list.setText("abilitylist")
        list.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.5)))
        list.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.3)))                
        list.setAlwaysOnTop(True)
        
        self.listmap = dict()

        
        for ability in list:
            self.additem(list,ability)
        list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAbility")
        
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
            toexecute.set(self.cunit)
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
        
        for eunit in s.unitmap.values():
            if not eunit.player ==self:
                sf.Application.debugText = str(unit) +"going after"+str(eunit)
                #s.framelistener.addToQueue(unit,Move(unit,eunit.node.getPosition()))
                map = dict()
                try:            
                    while not self.getHighest(map,unit,eunit).action:
                        print map
                except Exception,e:
                    print e
                s.turn.nextUnitTurn()
                break     
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
                if highest <abil.overallValue() and not map.has_key(abil):
                    highest = abil.overallValue()
                    hiabil = abil
        map[hiabil] = True            
        hiabil = copy.copy(hiabil)            
        hiabil.set(unit,eunit)
        s.framelistener.addToQueue(unit,hiabil)
        
        s.logger.info(str(unit)+" "+str(hiabil))
        return hiabil



    