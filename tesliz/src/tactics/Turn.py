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

        if self.pause:
            return
        if len(self.turnlist) > 0:
            self.nextUnitTurn()
            return
        
        for unit in s.unitmap.values():
            if unit.increment():
               self.turnlist.append(unit) 
               
    def nextUnitTurnUnpause(self):
        self.pause = False
        self.nextUnitTurn()    
    def nextUnitTurn(self):
        if not s.framelistener.getActiveQueue() == 0:        
            return
        if (s.framelistener.timer > 0.0) or s.ended or self.pause:
            return
        if len(self.turnlist)== 0:
            return
        self.pause = True
        s.framelistener.timer = 1
        unit =self.turnlist.pop()
        if unit.attributes.hitpoints <1:
            self.pause  = False
            return
            
        s.log(unit)
        s.framelistener.cplayer = unit.player
        
    
        unit.startTurn()           
    turnlist = []          

class RealTimeTurn(object):
    def __init__(self):
        s.turn = self
        
    def doTurn(self):
        if len(s.framelistener.unitqueues) == 0:
            for player in s.playermap.values():
                for unit in player.unitlist:
                    unit.startTurn()
    def nextUnitTurn(self):
        s.framelistener.cplayer = s.playermap["Player1"]
    def nextUnitTurnUnpause(self):
        self.pause = False
        self.nextUnitTurn()                        