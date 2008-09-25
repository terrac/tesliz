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
import random
s = Singleton()

class RandomUtterance:
    
    def __init__(self,unit,base):
        self.unit =unit
        self.base = base
    def execute(self,timer):
        battlecrymap = s.knowledge.getKnowledgeList(self.base,self.unit.knowledgelist)
        s.chatbox.add(battlecrymap[random.randrange(0,len(battlecrymap))],self.unit)


class Combat(object):
    
    
    def __init__(self,unit,getBest):
        self.unit =unit
        self.getBest = getBest
        self.running = True
        self.battlecry = RandomUtterance(unit,"battlecry")
        self.battlecry.called = False

    def getMentalCommands(self):
        pass


    def execute(self,timer):
        #aoeu
        unit = self.unit
        
        if not s.framelistener.isActive(self.unit):
            if not self.battlecry.called:
                self.battlecry.execute(timer)
                self.battlecry.called = True
        lodis = 999
        lounit = None
        for eunit in s.unitmap.values():            
            if not eunit.player ==unit.player:
                dis = distance(eunit.node.getPosition(),unit.node.getPosition())
                if dis < lodis:
                    lodis =dis
                    lounit = eunit
        if not lounit:                
            unit.mental.state["angry"] = 0
            return False
            
        eunit = lounit
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
            
        
        
        unit.mental.state["angry"] = 50#     
        return True
    



class Leader(object):
    
    
    def __init__(self,unit,endPos = None):
        self.unit =unit
        self.endPos = endPos
        self.bqueue =[]
        self.running = False

    def execute(self,timer):
        
        if self.unit.mental.state["angry"] > 10:
            return True
        unit = self.unit
        if s.framelistener.isActive(unit):
            return True
        s.chatbox.add("follow me",unit)
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
    
    
    def __init__(self,unit):
        self.unit =unit
        self.leader = None
        

  
        
    state = "calm"    
    running = False
    def broadcast(self,text,unit):
        if text == "follow me":
            self.running = True
            self.leader = unit
        if text == "stop following me":
            self.running = False
        
    def execute(self,timer):
        if not self.leader:
            return False
        if self.unit.mental.state["angry"] > 10:
            return True
        unit = self.unit
        if s.framelistener.isActive(unit):
            return True
        
        move = Move()
        setStart(move,unit,self.leader)
        s.framelistener.addToQueue(unit,move)
        
        return True

    #leader = property(None, setLeader, None, None)
        