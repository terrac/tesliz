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
               
        
    def nextUnitTurn(self):
        if not len(s.framelistener.unitqueues) == 0:        
            return
        if (s.framelistener.timer > 0.0) or s.ended or self.pause:
            return
        self.pause = True
        s.framelistener.timer = 1
        unit =self.turnlist.pop()
        s.logger.info(unit)
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