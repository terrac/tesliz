import sys
import copy
from tactics.Singleton import *
 
from tactics.datautil import *
from mental.commands import *

import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
from utilities.physics import *
import random
s = Singleton()

class RandomUtterance:
    
    def __init__(self,unit,type):
        self.unit =unit
        self.type = type
    def execute(self,timer):
        utterance = s.knowledge.getRandomFromParent(self.type,self.unit.knowledgelist)
        s.chatbox.add(utterance,self.unit)


class ExecuteList:
    def __init__(self,list):
        self.list = list
    
    def execute(self,unit):
        for x in self.list:
            x.execute(unit)
        
class BroadcastM:
    def __init__(self,text,to = "all"):        

        self.text = text
        self.to = to
            
    def execute(self,unit):        
        s.grammar.broadcast(self.text,unit,self.to)
        if self.to != "self":
            s.chatbox.add(self.text,unit)
        s.log(self.text,self)
        
class Response:
    
    def __init__(self,unit):
        self.unit =unit
        self.running = False

    def broadcast(self,text,unitbroadcastto,unitbroadcasting):
        
        text =text.split()[0]
        map = s.knowledge.getTypeMap(text,self.unit.knowledgelist)
        list =map.values()
        if len(list) > 0:
            map = list[random.randrange(0,len(list))]     
            #map = s.knowledge.getTypeMap(association.value,self.unit.knowledgelist)
            map.value.execute(self.unit)
            
        

        

#class Combat(object):
#    
#    
#    def __init__(self,unit,getBest):
#        self.unit =unit
#        self.getBest = getBest
#        self.running = True
#        self.battlecry = RandomUtterance(unit,"battlecry")
#        self.battlecry.called = False
#        
#
#    def getMentalCommands(self):
#        pass
#
#
#    def execute(self,timer):
#        #aoeu
#        unit = self.unit
#        
#        lodis = 999
#        lounit = None
#        for eunit in s.unitmap.values():            
#            if not eunit.player ==unit.player:
#                dis = distance(eunit.node.getPosition(),unit.node.getPosition())
#                if dis < lodis:
#                    lodis =dis
#                    lounit = eunit
#        if not lounit:                
#            unit.mental.state["angry"] = 0
#            return False
#        
#        
#        if not s.framelistener.isActive(self.unit):
#            if not self.battlecry.called:
#                self.battlecry.execute(timer)
#                self.battlecry.called = True
#                
#        s.framelistener.clearActions(self.unit)
#            
#        eunit = lounit
#        bool =False
#        
#        try:            
#            while not bool:
#                abil = self.getBest(unit)
#                
#                
#                if distance(eunit.body.getOgreNode().getPosition(), unit.body.getOgreNode().getPosition()) > abil.range:
#                    move = Move()
#                    setStart(move,unit,None,eunit.node.getPosition())
#                    s.framelistener.unitqueue.addToQueue(unit,move)
#                    
#                setStart(abil,unit,eunit)
#                s.framelistener.unitqueue.addToQueue(unit,copy.copy(abil))
#  #              print unit
#
# #               print unit.actionqueue
#                bool =abil.action
#        except Exception,e:
#            pass
#            #s.log( e,self.unit)
#            
#        
#        
#        unit.mental.state["angry"] = 50#     
#        return True
#    

class Leader(object):
    
    
    def __init__(self,unit,endPos = None):
        self.unit =unit
        self.endPos = endPos
        self.bqueue =[]
        self.running = True

    def execute(self,timer):
        if not self.endPos:
            return False
        if self.unit.mental.state["angry"] > 10:
            self.unit.body.freeze()
            return True
        unit = self.unit
        if s.framelistener.isActive(unit):
            
            return True
        s.chatbox.add("follow me",unit)
        move = Move()
        setStart(move,unit,None,self.endPos)
        s.framelistener.unitqueue.addToQueue(unit,move)
        if distance(unit.node.getPosition(),self.endPos) < 3:
            s.mental.broadcast("We are here",unit)
            return False
        return True

    def getMentalCommands(self):        
        return [BroadcastMessage("follow me","follow me",self.unit,"myside"),BroadcastMessage("stop following me","following me",self.unit,"myside")]

class Follower(object):
    
    
    def __init__(self,unit):
        self.unit =unit
        self.leader = None
        

  
        
    state = "calm"    
    running = False
    def broadcast(self,text,unitbroadcastto,unitbroadcasting):
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
        s.framelistener.unitqueue.addToQueue(unit,move)
        
        return True

    #leader = property(None, setLeader, None, None)
class FamilySupporter:
    def __init__(self,familylist,familyprotector = None):
        self.familylist = familylist
        self.familyprotector = familyprotector
        self.emap = {"fine" : Response("worry",50,"fear of spouse death"),}
        self.contextlist = []
    def broadcast(self,text,unitbroadcastto,unitbroadcasting):
        if unit == self.familyprotector:
            self.emap[text].setEmotion(self)
    def execute(self,timer):
        #combat recedes, wait for spouse
        #I was so worried about you
        #what about you?
        #ill stay here
        pass   

class FamilyProtector:
    def __init__(self,familylist):
        self.familylist = familylist   
        
                 
    def execute(self,timer):
        #angry - > combat
        # anger recedes = > find spouse
        #thank god you are ok
        #we will be fine, but stay here I've brought these troops to guard you
        #I will be fine.  I need to keep this castle safe though
        
        #keep track of family supporter pos
        pass         
class FamilyDependent:
    def __init__(self,familylist):
        self.familylist = familylist    
    def execute(self,timer):
        pass          