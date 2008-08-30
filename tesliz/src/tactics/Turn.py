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
               unit.startTurn() 
               self.pause=True
#    def startTurn(self):
#        self.s.playerlist.index(pnum).startTurn()
    
    
        
#    def endTurn(self, e):                         
#        pnum = self.pnum + 1 % len(self.s.playerlist)
#        if pnum == 0:   
#          for u in s.unitmap.values():
#             u.reset()              
#        return True            