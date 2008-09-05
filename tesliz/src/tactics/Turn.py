from tactics.Singleton import *
import logging
log = logging.getLogger('')
s = Singleton()
class Turn(object):
    
    
    
    pnum = 0
    
    def __init__(self):
        s.turn = self
        
    pause = False    
    def doTurn(self):
        
        if len(self.turnlist) > 0 and len(s.framelistener.unitqueues) == 0:
            self.nextUnitTurn()
        if self.pause:
            return
        for unit in s.unitmap.values():
            if unit.increment():
               self.turnlist.append(unit) 
               self.pause=True
        if self.pause:
            self.nextUnitTurn()
        
    def nextUnitTurn(self):
        if len(self.turnlist) == 0:
            self.pause = False
            return
        if (s.framelistener.timer > 0.0) or s.ended:
            return
        s.framelistener.timer = 1
        unit =self.turnlist.pop()
        s.logger.info(unit)
        s.framelistener.cplayer = unit.player
        unit.startTurn()           
    turnlist = []          
#    def startTurn(self):
#        s.playerlist.index(pnum).startTurn()
    
    
        
#    def endTurn(self, e):                         
#        pnum = self.pnum + 1 % len(s.playerlist)
#        if pnum == 0:   
#          for u in s.unitmap.values():
#             u.reset()              
#        return True            