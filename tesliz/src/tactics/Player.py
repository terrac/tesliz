from tactics.Singleton import *

class HumanPlayer(object):
        
    s = Singleton()
    hookid = "Player1"
    unitlist = []
    lastClick = None
    cunit = None
    def startTurn(self,unit):
       cunit = unit 
       self.s.framelistener.cunit = cunit
       self.s.framelistener.displayActions()
    
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

        
        item =CEGUI.ListboxTextItem ("move")
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listmap["move"]=item # we need to keep the listitems around for the list box to work
        list.addItem(item)
        item =CEGUI.ListboxTextItem ("attack")
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listmap["attack"]=item # we need to keep the listitems around for the list box to work
        list.addItem(item)
        
        item =CEGUI.ListboxTextItem ("endturn")
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listmap["endturn"]=item # we need to keep the listitems around for the list box to work
        list.addItem(item)
        
        list.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "handleAction")    
    listmap = dict()
    
    #move to player
    def handleAction(self, e):
        #aoeu dir(e.window.getFirstSelectedItem().getText())
        text = e.window.getFirstSelectedItem().getText()
        if text == "move":
            self.iexecute = Move(self.cunit.node,self.cunit.body,None)
        if text == "attack":
            self.iexecute = Move(self.cunit.node,self.cunit.body,None)
        if not isinstance(e.window,CEGUI.ListboxTextItem):    
            e.window.removeItem(e.window.getFirstSelectedItem())   
        if text == "endturn" or e.window.getItemCount() == 1:
            self.listmap = dict()
            CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")    
        return True
    def clickEntity(self,name,position):
        if self.iexecute:            
            self.iexecute.endPos = position
            self.runningexecutes.append(self.iexecute)
            iexecute = None    
     
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
        for eunit in s.unitmap.values():
            if not eunit.player ==self:
                s.framelistener.runningexecutes.append(Move(unit.node,eunit.node))
                break     
        #go through playremap and find closest enemy.  Set to attack
        a = 5       
       
            