import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *
#from data.traits.Generictraits import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
from utilities.physics import *
s = Singleton()

class Combat(object):
    
    
    def __init__(self,unit,getBest):
        self.unit =unit
        self.getBest = getBest

    def execute(self,timer):
        unit = self.unit
        
        if s.framelistener.isActive(unit):
            return True
        for eunit in s.unitmap.values():
            if not eunit.player ==unit.player and eunit.getVisible():
                #sf.Application.debugText = str(unit) +"going after"+str(eunit)
                #s.framelistener.addToQueue(unit,Move(unit,eunit.node.getPosition()))
                
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
                        bool =abil.action
                except Exception,e:
                    print e
                    
                
                s.turn.nextUnitTurnUnpause()
                break     
                return True           
        return False
    



class Leader(object):
    
    
    def __init__(self,unit,pos):
        self.unit =unit
        self.pos = pos

    def execute(self,timer):
        unit = self.unit
        if s.framelistener.isActive(unit):
            return True
        s.mental.broadcast("follow me")
        move = Move()
        setStart(move,unit,None,self.pos)
        s.framelistener.addToQueue(unit,move)
        if distance(unit.node.getPosition(),self.pos) < 3:
            s.mental.broadcast("We are here")
            return False
        return True
    