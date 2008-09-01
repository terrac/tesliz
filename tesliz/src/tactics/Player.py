import sys
from tactics.Singleton import *
from tactics.Move import *
from tactics.Attack import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
class HumanPlayer(object):
        
    s = Singleton()
    
    #Tells you what the id of the last cegui hooks for the framelistener was    
    hookid = "Player1"
    
    unitlist = []
    lastClick = None
    cunit = None
    iexecute = None
    def startTurn(self,unit):
       self.cunit = unit 
       #self.s.framelistener.cunit = cunit
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

        
        self.additem(list,"Move")
        self.additem(list,"Attack")
        self.additem(list,"EndTurn")
        for ability in self.cunit.abilities:
            self.additem(list,ability)
        list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAction")    
    listholder = []
    
    
    #move to player
    def handleAction(self, e):
        #aoeu dir(e.window.getFirstSelectedItem().getText())
        text = e.window.getFirstSelectedItem().getText()
        
        if self.cunit.abilities.has_key(text):
            showAbilityList(text);
        try:
            #eval(" Move(self.cunit)")
            ez = str(text+"(self.cunit)")
            self.iexecute = eval(ez)
        except Exception, ex:
             print repr(ex)
        if not isinstance(e.window,CEGUI.ListboxTextItem):    
            e.window.removeItem(e.window.getFirstSelectedItem())   
        if text == "EndTurn" or e.window.getItemCount() == 0:
            self.listmap = dict()
            CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
            s.turn.nextUnitTurn()    
            #import time
            #time.sleep(1)
        return True
    

    def clickEntity(self,name,position):
        if self.iexecute:
            unit = None
            if s.unitmap.has_key(name):
                unit = s.unitmap[name]           
            if not self.iexecute.setUnitAndPosition(unit,position):
                sf.Application.debugText = "Action failed"
                return
            sf.Application.debugText = "Action Succeeded"
            self.s.framelistener.runningexecutes.append(self.iexecute)
            self.iexecute = None    
    def additem(self,list,name):        
        item =CEGUI.ListboxTextItem (name)
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        list.addItem(item)
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
    unitlist = []
    s = Singleton()
    hookid = "Computer1"
    def startTurn(self,unit):
        for eunit in self.s.unitmap.values():
            if not eunit.player ==self:
                self.s.framelistener.runningexecutes.append(Move(unit,eunit.node.getPosition()))
                self.s.framelistener.runningexecutes.append(Attack(unit,eunit))
                self.s.turn.nextUnitTurn()
                break     
        #go through playremap and find closest enemy.  Set to attack
       # a = 5       
       
            