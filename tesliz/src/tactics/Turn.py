from tactics.Singleton import *

class Turn(object):
    
    s = Singleton()
    
    pnum = 0
    
    def __init__(self):
        self.s.turn = self
        
    pause = False    
    def doTurn(self):
        if self.pause:
            return
        for unit in self.s.unitmap.values():
            if unit.increment():
               self.turnlist.append(unit) 
               self.pause=True
        if self.pause:
            nextUnitTurn()
        
    def nextUnitTurn(self):
        if len(turnlist) == 0:
            self.pause = False
            return
        
        unit =turnlist.pop()
        unit.startTurn()           
    turnlist = []          
#    def startTurn(self):
#        self.s.playerlist.index(pnum).startTurn()
    
    
        
#    def endTurn(self, e):                         
#        pnum = self.pnum + 1 % len(self.s.playerlist)
#        if pnum == 0:   
#          for u in s.unitmap.values():
#             u.reset()              
#        return True            