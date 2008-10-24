from tactics.Singleton import *
from tactics.util import *
s = Singleton()



def isWantedHurt(eunit,unit):
    return eunit.player ==unit.player and eunit.attributes.hitpoints < eunit.attributes.maxhitpoints

def isWanted(eunit,unit):
    return eunit.player !=unit.player 

def getClose(unit,isWanted):

    lodis = 999
    lounit = None
    for eunit in s.unitmap.values():            
        if isWanted(eunit,unit):
            dis = distance(eunit.node.getPosition(),unit.node.getPosition())
            if dis < lodis:
                lodis =dis
                lounit = eunit

    return lounit

def getBest(unit,isValid):
    best = None
    for trait in unit.traits.values():
       for ability in trait.getClassList():
           if isValid(ability):
               if not best:
                   best = ability                
               elif best.value <ability.value:
                   best = ability
                   
    return best
class Combat(object):
    
    
    def __init__(self,unit,isValid, isWanted):
        self.unit =unit
        self.isValid = isValid
        self.running = True
        #if getClose:
        self.isWanted = isWanted
#        else:
#            self.getClose combat.getClose
        


    
    def execute(self,timer):
        #aoeu
        unit = self.unit
        eunit = getClose(unit,self.isWanted)

        if not eunit:                
        
            return False
        
        
    
        s.framelistener.clearActions(self.unit)
        
        
        bool =False
        
        
        while not bool:
            abil = getBest(unit,self.isValid)
            if not abil:
                aoeu
            
            if distance(eunit.body.getOgreNode().getPosition(), unit.body.getOgreNode().getPosition()) > abil.range:
                move = Move()
                setStart(move,unit,None,eunit.node.getPosition())
                s.framelistener.addToQueue(unit,move)
                
            if not setStart(abil,unit,eunit):
                break # wasnt in range, maybe look for other abilites later 
            s.framelistener.addToQueue(unit,copy.copy(abil))

            try:
                bool =abil.action
            except Exception,e:                
                s.log( e,self.unit)
                break;
        
        
        unit.mental.state["angry"] = 50#     
        return True
    
