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
    hookid = "Computer1"
    def startTurn(self,unit):    
        #go through playremap and find closest enemy.  Set to attack
        a = 5       
       
            