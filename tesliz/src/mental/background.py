import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *
from mental.commands import *

import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
from utilities.physics import *
s = Singleton()

class Combat(object):
    
    
    def __init__(self,unit,getBest):
        self.unit =unit
        self.getBest = getBest
       # s.turnbased = True
        #self.bqueue =[]
        #self.cfightvalue = 0

    def getMentalCommands(self):
        pass
#    def setup(self,unit,eunit):
#        #if self.cfightvalue and self.cfightvalue-eunit.value >10:
#        #    return False
#        #else:
#        unit = self.unit
#        
#        
#        s.framelistener.addToBackground(self,self)
#        s.framelistener.clearActions(unit)
#        #    self.cfightvalue = eunit.value


    def execute(self,timer):
        #aoeu
        unit = self.unit
         
        if s.framelistener.isActive(unit):
            print "aoeu"
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
                    s.log( e,self)
                    
                
                s.turn.nextUnitTurnUnpause()
                unit.mental.state["angry"] = 50#     
                return True
        unit.mental.state["angry"] = 0
        s.turnbased = False           
        return False
    



class Leader(object):
    
    
    def __init__(self,unit,endPos = None):
        self.unit =unit
        self.endPos = endPos
        self.bqueue =[]

    def execute(self,timer):
        if self.unit.mental.state["angry"] > 10:
            return True
        unit = self.unit
        if s.framelistener.isActive(unit):
            return True
        s.chatbox.broadcast("follow me",unit)
        move = Move()
        setStart(move,unit,None,self.pos)
        s.framelistener.addToQueue(unit,move)
        if distance(unit.node.getPosition(),self.pos) < 3:
            s.mental.broadcast("We are here",unit)
            return False
        return True

    def getMentalCommands(self):        
        return [BroadcastMessage("follow me","follow me",self.unit),BroadcastMessage("stop following me","following me",self.unit)]

class Follower(object):
    
    
    def __init__(self,unit,leader):
        self.unit =unit
        self.leader = leader
        

    def execute(self,timer):
        if self.unit.mental.state["angry"] > 10:
            return True
        unit = self.unit
        if s.framelistener.isActive(unit):
            return True
        
        move = Move()
        setStart(move,unit,leader)
        s.framelistener.addToQueue(unit,move)
        
        return True
        