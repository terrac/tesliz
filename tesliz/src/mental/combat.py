from tactics.Singleton import *
from tactics.util import *
s = Singleton()


def getClose(unit):
    
    lodis = 999
    lounit = None
    for eunit in s.unitmap.values():            
        if not eunit.player ==unit.player:
            dis = distance(eunit.node.getPosition(),unit.node.getPosition())
            if dis < lodis:
                lodis =dis
                lounit = eunit
    return lounit

def getCloseHurt(unit):

    lodis = 999
    lounit = None
    for eunit in s.unitmap.values():            
        if eunit.player ==unit.player and eunit.attributes.hitpoints < eunit.attributes.maxhitpoints:
            dis = distance(eunit.node.getPosition(),unit.node.getPosition())
            if dis < lodis:
                lodis =dis
                lounit = eunit

    return lounit

class Combat(object):
    
    
    def __init__(self,unit,getBest, getClose):
        self.unit =unit
        self.getBest = getBest
        self.running = True
        #if getClose:
        self.getClose = getClose
#        else:
#            self.getClose combat.getClose
        


    def execute(self,timer):
        #aoeu
        unit = self.unit
        eunit = self.getClose(unit)

        if not eunit:                
        
            return False
        
        
    
        s.framelistener.clearActions(self.unit)
            
        
        bool =False
        
        try:            
            while not bool:
                abil = self.getBest(unit)
                
                
                if distance(eunit.body.getOgreNode().getPosition(), unit.body.getOgreNode().getPosition()) > abil.range:
                    move = Move()
                    setStart(move,unit,None,eunit.node.getPosition())
                    s.framelistener.addToQueue(unit,move)
                    
                setStart(abil,unit,eunit)
                s.framelistener.addToQueue(unit,copy.copy(abil))
  #              print unit

 #               print unit.actionqueue
                bool =abil.action
        except Exception,e:
            pass
            #s.log( e,self.unit)
            
        
        
        unit.mental.state["angry"] = 50#     
        return True
    
